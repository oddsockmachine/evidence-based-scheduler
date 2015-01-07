from random import randint, shuffle, choice
from pprint import pprint


team_members = ["anna", "bill", "cass", "dave"]
num_team_members = len(team_members)

num_issues_completed = 20
num_issues_total = 40

issues = {}
for i in range(num_issues_completed):
    issues[i] = {
                 "estimates":{name: randint(1,10) for name in team_members},
                 "time_taken": randint(1,10),
                 "completed":True,
                 "completed_by": team_members[randint(0, num_team_members)],
                }
for i in range(num_issues_completed, num_issues_total):
    issues[i] = {
                 "estimates":{name: randint(1,10) for name in team_members},
                 "time_taken": 0,
                 "completed":False,
                 "completed_by": None,
                }

# pprint(issues)

team_estimates = {team_member: [issue['estimates'][team_member]
                               for issue in issues.itervalues() if issue['completed']]
                  for team_member in team_members}
# pprint(team_estimates)

team_velocities = {team_member: [issue['estimates'][team_member]/float(issue['time_taken'])
                               for issue in issues.itervalues() if issue['completed']]
                  for team_member in team_members}

# pprint(team_velocities)


todo_issue_ids = [_id for _id, issue in issues.iteritems() if not issue['completed']]
done_issue_ids = [_id for _id, issue in issues.iteritems() if issue['completed']]

num_simulations = 100
total_estimates = []

for sim in range(num_simulations):
    shuffle(todo_issue_ids)
    total = 0
    for issue_id in todo_issue_ids:
        team_member = team_members[randint(0, num_team_members)]
        random_estimate = issues[issue_id]['estimates'][team_member]
        random_velocity = choice(team_velocities[team_member])
        predicted_time = random_estimate/float(random_velocity)
        total += predicted_time
    total_estimates.append(int(total))

total_estimates.sort()

print total_estimates[25]
print total_estimates[50]
print total_estimates[75]