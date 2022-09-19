function network(){

  alert("Network not available now")

}

function apply(){
  window.location="apply.html";

  }
  function transfer(){
  window.location="transfer.html";
}
function success(){
  alert("Loan request submitted successfully")
}
function profile(){
  window.location="profile.html";
}


function validate(){
  var home = document.getElementById("Haddress").value
  var office = document.getElementById("Oaddress").value
  var city= document.getElementById("city").value
  var card = document.getElementById("card").value



  if (home == "") 
    {
            alert("field value missing");
        return false;
    }
    if (office == "") 
    {
            alert("field value missing");
        return false; 
    }
   
    if (city == "") 
    {
            alert("field value missing");
        return false;
    }
    
    if (card == "") 
    {
            alert("field value missing");
        return false;
    }
}