let flag = false
let valuee = sessionStorage.getItem("IBM_WAC_DEVICE_ID")

if(valuee == null)
{
    flag = false
}
else {
    flag = true
}

let listitems = ""
if(flag === true)
{
    listitems+=`
        <a href="/profile" class="btn btn-info me-3">Profile</a>
        <a href="/viewJobs" class="btn btn-info me-3">View Jobs</a>
        <a href="/recommend" class="btn btn-info me-3">Recommend</a>
        <a href="/logout" class="btn btn-info me-3">Logout</a>      
    `
}
else if(flag===false){
    listitems+=`
        <a href="/register" class="btn btn-info me-3">Register</a>
        <a href="/login" class="btn btn-info me-3">Login</a>
    `
}

document.getElementById("navlist").innerHTML = listitems


