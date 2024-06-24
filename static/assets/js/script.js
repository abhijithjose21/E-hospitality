

function showAlert(){


var first_name = document.getElementById('first_name').value;
var last_name = document.getElementById('last_name').value;
var date_of_birth = document.getElementById('date_of_birth').value;
var phone_number = document.getElementById('phone_number').value;
var address = document.getElementById('address').value;
var username = document.getElementById('user_name').value;
var password = document.getElementById('password').value;
var con_password = document.getElementById('con_password').value;

if(!first_name || !last_name || !date_of_birth || !phone_number || !address || !user_name || !password || !con_password){

alert('please fill out required field');
}
else{

alert("Registration Successful.Now you can Register");

}

}

function doctorAlert(){

var name = document.getElementById('name').value;
var department = document.getElementById('department').value;
var username = document.getElementById('user_name').value;
var password = document.getElementById('password').value;
var con_password = document.getElementById('con_password').value;

if(!name || !department || !user_name || !password || !con_password){

alert('please fill out required field');
}
else{

alert("Registration Successful.");

}
}