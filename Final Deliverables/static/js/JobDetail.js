import data from '../index.json' assert { type: "json" };

let index = document.getElementById("mainthing").value
let jobdesc = data[index-1]

let pair = {
    0:"HTML,CSS,JS",
    1:"Communication",
    2:"Python",
    3:"C,C++",
    4:"Java",
    5:"UI/UX",
    6:"Node JS",
    7:"React JS",
    8:"MySQL",
    9:"AWS"
}
let skillsetString = jobdesc.skill.toString()
console.log(typeof(skillsetString))
let  skillString = skillsetString.split('')
console.log(skillString)
let detail  = ""
detail+=`
<div>
    <h2>Job Role : ${jobdesc.jobRole}</h2>
    <p>Company Name : ${jobdesc.companyName}</p>
    <p>Job Location : ${jobdesc.jobLocation}</p>
    <p>Job Description : ${jobdesc.jobDescription}</p>
    <p>Posted At: ${jobdesc.postedAt.toLocaleString().slice(0,10)}</p>


</div>
`

let str = ""
skillString.map((item)=>{
    console.log(item)
    str+=`
    <li>${pair[item]}</li>
`
})

let links = ""
links+=`
    <a href="/applyJob/${index}" class="btn btn-success" >Apply Here</a>
`
document.getElementById("applyLink").innerHTML = links
document.getElementById("skillss").innerHTML = str
document.getElementById("jobDetailBox").innerHTML =detail