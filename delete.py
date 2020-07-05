import os,shutil

li = ["video1_frames","video2_frames","swappedframes","inputs"]
for i in li:
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	print(BASE_DIR)
	dir = os.path.join(BASE_DIR, i)
	print(dir)
	for root, dirs, files in os.walk(dir):
	  for di in dirs:
	  	print(di)
	  	shutil.rmtree(os.path.join(dir,di))
	  for file in files:
	    path = os.path.join(dir, file)
	    print(path)
	    os.unlink(path)


os.makedirs("video1_frames/landmarks")
os.makedirs("video2_frames/landmarks")

os.remove("Output.mp4")
