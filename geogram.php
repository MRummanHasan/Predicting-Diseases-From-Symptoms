<?php

echo "<h2>PHP is API setup!</h2>";

// $location_val = $_GET['location'];
// echo $location_val;
// $abc="hehe";

$myjson = "http://localhost:8001/full/";
$maps_json = file_get_contents($myjson); 
echo $maps_json;




//i hope this curl approach works

// THIS SNIPPET to se will send your data to the api once get posted just a little thing i have
if (isset($_POST['submit'])){
    echo "Post hoja ab  jee?";
        $url = 'http://localhost:8001/postData';
        $data = array('name' => $_POST['location']);

        //yahan per dkh uper array me jo value hai uss ka name hai thek hai
        // ab neechy dkh
        //API URL
       // $url = 'http://www.example.com/api';

        //create a new cURL resource
        $ch = curl_init($url);

        //setup request to send json via POST
        // $data = array(
        //     'username' => 'codexworld',
        //     'password' => '123456'
        // );
        $payload = json_encode(array("data" => $data));
            // yahan pe double ha   mey ye nhi smjha tm kro, jo krna chah rhy ho
        //attach encoded JSON string to the POST fields
        curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);

        //set the content type to application/json
        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type:application/json'));

        //return response instead of outputting
         curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);


         
//ab kr is echo ney 1 print kia screen pr
        //execute the POST request
        $result = curl_exec($ch);
             echo $result; //ismy direct result arha hy; to? jbky hamain yahan wo value chahihy hy, jo function hamara return kr rha ho
            //ab dkh
 // url to change kr bhi jbhi to ayega
            //close cURL resource
        curl_close($ch);

        // // use key 'http' even if you send the request to https://...
        // $options = array(
        //     'http' => array(
        //         'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
        //         'method'  => 'POST',
        //         'content' => http_build_query($data),
        //     ),
        // );
        // $context  = stream_context_create($options);
        // $result = file_get_contents($url, false, $context);

        // var_dump($result);
}

// $maps_array = json_decode($maps_json,true);
// echo $maps_array['naam'];
?>
<!DOCTYPE html>
<html lang="en">
<head>

<script>
// this code is more efficient like if you donot want your page tp refresh then use this one
function sendData(){
    console.log("sendData() is called"); // just to check if the function is called or not now you // //can refresh the page and use it and also restart the api
    var v = $.ajax({
    url: "./geogram.php",  // if this fail use /geogram.php or geogram.php
      method: "POST",
    dataType: "text",
    data: $("nameForm").serialize(),   
    success : function(response){
     console.log("response"); 
   }
  });
}
</script>

<title>Rumi</title>
<meta charset="utf-8">
</head>
<body>
<form id="nameForm" action="geogram.php" method="POST">
    <input type="text" name="location"/>
    <button type="submit" name="submit" >Yes</button>
  
<br>
<br>
<br>
</form>



</body>
</html>
