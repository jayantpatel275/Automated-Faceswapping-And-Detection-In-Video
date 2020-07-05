# Importing 

import cv2
import dlib
import numpy as np
import sys
import os
from os.path import isfile, join

# Video to Frames 

filename = 'inputs/input_video1.mp4'
# filename = sys.argv[1]
vidcap = cv2.VideoCapture(filename)
success,image = vidcap.read()
count = 0
success = True
while count!=100:
  success,image = vidcap.read()
  cv2.imwrite("video1_frames/frame%d.jpg" % count, image)     # save frame as JPEG file
  if cv2.waitKey(10) == 27:                     # exit if Escape is hit
      break
  count += 1

filename = 'inputs/input_video2.mp4'
# filename = sys.argv[2]
vidcap = cv2.VideoCapture(filename)
success,image = vidcap.read()
count = 0
success = True
while count!=100:
  success,image = vidcap.read()
  cv2.imwrite("video2_frames/frame%d.jpg" % count, image)     # save frame as JPEG file
  if cv2.waitKey(10) == 27:                     # exit if Escape is hit
      break
  count += 1

  # Frames to landmarks

PREDICTOR_PATH = "shape_predictor_81_face_landmarks.dat"
predictor = dlib.shape_predictor(PREDICTOR_PATH)
detector = dlib.get_frontal_face_detector()

class TooManyFaces(Exception):
    pass

class NoFaces(Exception):
    pass

def get_landmarks(im):
    rects = detector(im, 1)

    if len(rects) > 1:
        raise TooManyFaces
    if len(rects) == 0:
        raise NoFaces
    return np.matrix([[p.x, p.y] for p in predictor(im, rects[0]).parts()])


for i in range(0,100):
    input_image = ('./video1_frames/frame%d.jpg'%i)
    image = cv2.imread(input_image)
    landmarks = get_landmarks(image)

    input_image = input_image[:-4]
    mat = np.matrix(landmarks)
    with open('video1_frames/landmarks/frame%d.txt'%i, 'w+') as f:
        for line in mat:
            np.savetxt(f, line, fmt='%.2d')
            
for i in range(0,100):
    input_image = ('./video2_frames/frame%d.jpg'%i)
    image = cv2.imread(input_image)
    landmarks = get_landmarks(image)

    input_image = input_image[:-4]
    mat = np.matrix(landmarks)
    with open('video2_frames/landmarks/frame%d.txt'%i, 'w+') as f:
        for line in mat:
            np.savetxt(f, line, fmt='%.2d')


# Swapping faces in frames

# Read points from text file
def readPoints(path) :
    # Create an array of points.
    points = [];
    
    # Read points
    with open(path) as file :
        for line in file :
            x, y = line.split()
            points.append((int(x), int(y)))
    

    return points

# Apply affine transform calculated using srcTri and dstTri to src and
# output an image of size.
def applyAffineTransform(src, srcTri, dstTri, size) :
    
    # Given a pair of triangles, find the affine transform.
    warpMat = cv2.getAffineTransform( np.float32(srcTri), np.float32(dstTri) )
    
    # Apply the Affine Transform just found to the src image
    dst = cv2.warpAffine( src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

    return dst


# Check if a point is inside a rectangle
def rectContains(rect, point) :
    if point[0] < rect[0] :
        return False
    elif point[1] < rect[1] :
        return False
    elif point[0] > rect[0] + rect[2] :
        return False
    elif point[1] > rect[1] + rect[3] :
        return False
    return True


#calculate delanauy triangle
def calculateDelaunayTriangles(rect, points):
    #create subdiv
    subdiv = cv2.Subdiv2D(rect);
    
    # Insert points into subdiv
    for p in points:
        subdiv.insert(p) 
    
    triangleList = subdiv.getTriangleList();
    
    delaunayTri = []
    
    pt = []    
        
    for t in triangleList:        
        pt.append((t[0], t[1]))
        pt.append((t[2], t[3]))
        pt.append((t[4], t[5]))
        
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])        
        
        if rectContains(rect, pt1) and rectContains(rect, pt2) and rectContains(rect, pt3):
            ind = []
            #Get face-points (from 68 face detector) by coordinates
            for j in range(0, 3):
                for k in range(0, len(points)):                    
                    if(abs(pt[j][0] - points[k][0]) < 1.0 and abs(pt[j][1] - points[k][1]) < 1.0):
                        ind.append(k)    
            # Three points form a triangle. Triangle array corresponds to the file tri.txt in FaceMorph 
            if len(ind) == 3:                                                
                delaunayTri.append((ind[0], ind[1], ind[2]))
        
        pt = []        
            
    
    return delaunayTri
        

# Warps and alpha blends triangular regions from img1 and img2 to img
def warpTriangle(img1, img2, t1, t2) :

    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))

    # Offset points by left top corner of the respective rectangles
    t1Rect = [] 
    t2Rect = []
    t2RectInt = []

    for i in range(0, 3):
        t1Rect.append(((t1[i][0] - r1[0]),(t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))
        t2RectInt.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))


    # Get mask by filling triangle
    mask = np.zeros((r2[3], r2[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(t2RectInt), (1.0, 1.0, 1.0), 16, 0);

    # Apply warpImage to small rectangular patches
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    #img2Rect = np.zeros((r2[3], r2[2]), dtype = img1Rect.dtype)
    
    size = (r2[2], r2[3])

    img2Rect = applyAffineTransform(img1Rect, t1Rect, t2Rect, size)
    
    img2Rect = img2Rect * mask

    # Copy triangular region of the rectangular patch to the output image
    img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] * ( (1.0, 1.0, 1.0) - mask )
     
    img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] + img2Rect 
    

# if __name__ == '__main__' :
    
#     # Make sure OpenCV is version 3.0 or above
#     (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

#     if int(major_ver) < 3 :
#         print >>sys.stderr, 'ERROR: Script needs OpenCV 3.0 or higher'
#         sys.exit(1)
            
for z in range(0,100):
    # Read images
    filename1 = 'video1_frames/frame%d.jpg'%z
    filename2 = 'video2_frames/frame%d.jpg'%z

    img1 = cv2.imread(filename1)
    img2 = cv2.imread(filename2)

    img1Warped = np.copy(img2)    

    # Read array of corresponding points
    points1 = readPoints('video1_frames/landmarks/frame%d.txt'%z)
    points2 = readPoints('video2_frames/landmarks/frame%d.txt'%z)    

    # Find convex hull
    hull1 = []
    hull2 = []

    hullIndex = cv2.convexHull(np.array(points2), returnPoints = False)

    for i in range(0, len(hullIndex)):
        hull1.append(points1[int(hullIndex[i])])
        hull2.append(points2[int(hullIndex[i])])

    # Find delanauy traingulation for convex hull points
    sizeImg2 = img2.shape
    rect = (0, 0, sizeImg2[1], sizeImg2[0])

    dt = calculateDelaunayTriangles(rect, hull2)

    if len(dt) == 0:
        quit()

    # Apply affine transformation to Delaunay triangles
    for i in range(0, len(dt)):
        t1 = []
        t2 = []

        #get points for img1, img2 corresponding to the triangles
        for j in range(0, 3):
            t1.append(hull1[dt[i][j]])
            t2.append(hull2[dt[i][j]])

        warpTriangle(img1, img1Warped, t1, t2)


    # Calculate Mask
    hull8U = []
    for i in range(0, len(hull2)):
        hull8U.append((hull2[i][0], hull2[i][1]))

    mask = np.zeros(img2.shape, dtype = img2.dtype)  

    cv2.fillConvexPoly(mask, np.int32(hull8U), (255, 255, 255))

    r = cv2.boundingRect(np.float32([hull2]))    

    center = ((r[0]+int(r[2]/2), r[1]+int(r[3]/2)))


    # Clone seamlessly.
    output = cv2.seamlessClone(np.uint8(img1Warped), img2, mask, center, cv2.NORMAL_CLONE)

    cv2.imwrite('swappedframes/frame%d.jpg'%z, output)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


# Frames to Video
 
def convert_frames_to_video(pathIn,pathOut,fps):
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
 
    #for sorting the file names properly
    files.sort(key = lambda x: int(x[5:-4]))
 
    for i in range(len(files)):
        filename=pathIn + files[i]
        #reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
#         print(filename)
        #inserting the frames into an image array
        frame_array.append(img)
 
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
 
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()
 
# if __name__=="__main__":
pathIn= './swappedframes/'
pathOut = 'Output.mp4'
fps = 25.0
convert_frames_to_video(pathIn, pathOut, fps)
 

