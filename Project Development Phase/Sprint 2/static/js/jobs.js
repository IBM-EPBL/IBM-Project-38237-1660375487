import data from '../index.json' assert { type: "json" };

let html=""
data.map((item,index)=>{
   let itemDate = new Date(item.postedAt)
   let jobrole = item.jobRole
    html+=`
    <div class="jobCard" accesskey=${index}>
        <h6><i class="bi bi-person-badge"></i>       ${item.jobRole}</h6>
        <p><i class="bi bi-building"></i>       ${item.companyName}</p>
        <p><i class="bi bi-calendar-check"></i>       ${itemDate.toLocaleString().slice(0,9)}</p>
        <a type="button" class="btn btn-success"  href="/viewDetail/${item.id}">
        View JD
      </a>
      <a type="button" class="btn btn-danger"  href="/viewJobs">
      Apply Job
    </a>                    
    </div>
    
    `
})
document.getElementById("main").innerHTML = html