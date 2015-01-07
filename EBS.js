function randInt(index, lower) {
    return Math.floor(Math.random()*lower+index)
}

function createEstimateDict(members) {
    estimates = {}
    members.forEach(function(member){
        estimates[member] = randInt(1, 10)
    })
    return estimates
}

team_members = ["anna", "bill", "cass", "dave"]
num_team_members = team_members.length

num_issues_total = 40
num_issues_completed = 20
issues = {}

for(var i=1; i<num_issues_completed; i++) {
    issues[i] = {
        "estimates": createEstimateDict(team_members),
        "time_taken": randInt(1, 10),
        "completed":true,
        "completed_by": team_members[randInt(0, num_team_members)],
    }
}


for(var i=num_issues_completed; i<num_issues_total; i++) {
    issues[i] = {
        "estimates": createEstimateDict(team_members),
        "time_taken": randInt(1, 10),
        "completed":false,
        "completed_by": "",
    }
}


//Extract all the estimates each team member gave for all issues.
team_estimates = {}
team_members.forEach(function(member) {
    // member = team_members[name]
    console.log(member)
    estimates = []
    Object.keys(issues).forEach(function(id) {
        issue = issues[id]
        if(issue.completed) {
            estimates.push(issue.estimates[member])
        }
    })
    team_estimates[member] = estimates
})

console.log(team_estimates)