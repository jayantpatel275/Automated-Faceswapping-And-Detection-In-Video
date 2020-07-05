
<!DOCTYPE HTLM>
<html>
<head>
	<link href="bootstrap.css" rel="stylesheet" type="text/css" media="all" />
	<title>FaceApp</title></head>
<body>

<nav class="navbar navbar-default">
  <div class="container-fluid">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="app.php">FaceApp</a>
    </div>
  </div>
</nav>


<center>
<form action="upload_video.php" method="post" enctype="multipart/form-data">
<table border="1px" width="922px"> 
		<tr>
			 <td style="padding:20px"><h4>Subject Video : </h4><input type="file" id="real-file" name="vid1"> </input></td>
			 <td><h4>Base Video : </h4><input type="file" id="real-file" name="vid2"> </input></td>
 			<td style="padding:10px"><br><center><input type="submit" name="submit" value="Upload" class="btn btn-md btn-primary"/></center></form></td>
		</tr>
		<tr>
			<td colspan="3" style="padding:20px"><font color="red"><h4>Note : Processing can take upto 2 - 10 minutes</h4></font></td>
		</tr>
</table>
<table border="1px">
		<tr>
			<td style="padding:20px"><center><h2>Subject Video</h2></center></td>
			<td style="padding:20px"><center><h2>Base Video</h2></center></td>
		</tr>
		<tr>
			<td style="padding:20px">
				<center>
				<video width="420" height="240" controls>
				  <source src="inputs/input_video1.mp4" type="video/mp4">
				Your browser does not support the video tag.
				</video>
				</center>
			</td>
			<td style="padding:20px">
				<center>
				<video width="420" height="240" controls>
				  <source src="inputs/input_video2.mp4" type="video/mp4">
				Your browser does not support the video tag.
				</video>
				</center>
			</td>
		<tr>
			<td colspan="2" style="padding:20px"><hr><center><h2>Output Video</h2></center></td>
		</tr>
		<tr>	
			<td colspan="2" style="padding:20px">	
				<center>
				<video width="820" height="350" controls>
				  <source src="Output.mp4" type="video/mp4">
				Your browser does not support the video tag.
				</video>
				</center>
			</td>
		</tr>
		<tr>
			<td colspan="2" style="padding:20px"><center><form action="delete.php" method="post"><font color="red"><h4>Note : Please Click  <input type="submit" name="submit" value="Clear" class="btn btn-md btn-primary"/>  after completion.</h4></font>
			</form></center>
			</td>
		</tr>
</table>
</center><br>
<footer class="page-footer font-small blue">
  <div class="footer-copyright text-center py-3">© 2019 Copyright :
    <a href="https://github.com/amvkind/"> amvkind </a>
  </div>
</footer><br>
</body>
</html>





