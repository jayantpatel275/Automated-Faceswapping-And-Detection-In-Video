<?php

shell_exec("python delete.py");
header("Cache-Control: no-cache, no-store, must-revalidate"); // HTTP 1.1.
header("Pragma: no-cache"); // HTTP 1.0.
header("Expires: 0");
header("Location: http://localhost/FaceSwapper/app.php");

?>