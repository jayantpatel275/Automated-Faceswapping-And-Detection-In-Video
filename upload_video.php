<?php
if (($_FILES['vid1']['name']!="")){
// Where the file is going to be stored
	//$target_dir = "upload/";
	$file = $_FILES['vid1']['name'];
	$path = pathinfo($file);
	$filename = "input_video1";
	$ext = $path['extension'];
	$temp_name = $_FILES['vid1']['tmp_name'];
	$path_filename_ext = "C:\\\\xampp\htdocs\\FaceSwapper\\inputs\\".$filename.".".$ext;
 
// Check if file already exists
if (file_exists($path_filename_ext)) {
 echo "Sorry, file already exists.";
 }else{
 move_uploaded_file($temp_name,$path_filename_ext);
 // echo "Congratulations! File Uploaded Successfully.";
 }
}

if (($_FILES['vid2']['name']!="")){
// Where the file is going to be stored
	//$target_dir = "upload/";
	$file = $_FILES['vid2']['name'];
	$path = pathinfo($file);
	$filename = "input_video2";
	$ext = $path['extension'];
	$temp_name = $_FILES['vid2']['tmp_name'];
	$path_filename_ext = "C:\\\\xampp\htdocs\\FaceSwapper\\inputs\\".$filename.".".$ext;
 
// Check if file already exists
if (file_exists($path_filename_ext)) {
 echo "Sorry, file already exists.";
 }else{
 move_uploaded_file($temp_name,$path_filename_ext);
 // echo "Congratulations! File Uploaded Successfully.";
 shell_exec("python main.py");
 }
}

header("Location: http://localhost/FaceSwapper/app.php");
?>

