console.log("HELLO");

function closeFlash() {
    console.log("working");
    var msg = document.getElementById("msg")
    msg.style.width = "0";
    msg.style.border = "0";
    msg.textContent = "";
  }
  