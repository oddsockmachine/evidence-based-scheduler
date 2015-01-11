from random import randint, shuffle, choice, random
from pprint import pprint
import json

def pick_random_team_member(members, proportions):
    total = 0.0
    cumulative_proportions = {}
    chosen_member = ""
    rand = random()
    for name, proportion in proportions.items():
        total += proportion
        cumulative_proportions[name] = total
        if total >= rand:
            chosen_member = name
            break
    return chosen_member

def write_random_issues_to_file(filename):
    # Create some completed example issues
    for i in range(num_issues_completed):
        issues[i] = {
                     "estimates":{name: randint(1,10) for name in team_members},  # Record what each team member estimated this issue as
                     "time_taken": randint(1,10),  # What was the time spent on this issue?
                     "completed":True,
                     "completed_by": team_members[randint(0, num_team_members-1)],  # Done by a random team member
                    }
    # Create some incomplete example issues
    for i in range(num_issues_completed, num_issues_total):
        issues[i] = {
                     "estimates":{name: randint(1,10) for name in team_members},
                     "time_taken": 0,
                     "completed":False,
                     "completed_by": None,
                    }

    # pprint(issues)
    with open("issues.json", 'w') as json_file:
        json_file.write(json.dumps(issues))
    return

def load_issues_from_file(filename):
    with open(filename, 'r') as json_file:
        issues = json.loads("".join(json_file.readlines()))
    return issues

def calculate_team_member_estimates(team_members, issues):
    """
    Extract all the estimates each team member gave for all issues
    """
    team_estimates = {team_member: [issue['estimates'][team_member]
                                   for issue in issues.itervalues() if issue['completed']]
                      for team_member in team_members}
    return team_estimates

def calculate_team_velocities(team_members, issues):
    """
    Calculate a list of velocities each team member achieved
    This is the ratio of estimated time to real time
    """
    team_velocities = {team_member: [issue['estimates'][team_member]/float(issue['time_taken'])
                                   for issue in issues.itervalues() if issue['completed']]
                      for team_member in team_members}
    return team_velocities

def calculate_uptake_rate(team_members, issues):
    """
    Calculate the proportion of issues completed per team member
    """
    team_uptake_rate = {name: len([issue for issue in issues.values() if issue['assigned_to'] == name])/
                              float(len([issue for issue in issues.values() if issue['assigned_to']]))
                        for name in team_members}
    return team_uptake_rate

def get_todo_ids(issues):
    """Return a list of IDs of issues that are still todo"""
    todo_issue_ids = [_id for _id, issue in issues.iteritems() if not issue['completed']]
    return todo_issue_ids

def get_done_ids(issues):
    """Return a list of IDs of issues that are completed"""
    done_issue_ids = [_id for _id, issue in issues.iteritems() if issue['completed']]
    return done_issue_ids

def run_monte_carlo_simulation(num_simulations, issues, team_members, team_velocities, team_uptake_rate, todo_issue_ids, done_issue_ids):
    total_estimates = []  # A list of estimates for the whole project
    num_team_members = len(team_members)

    for sim in range(num_simulations):
        shuffle(todo_issue_ids)  # Shuffle the issues so we sample them in a random order
        total = 0  # Amount of time estimated to complete project
        for issue_id in todo_issue_ids:
            if issues[issue_id]['assigned_to'] != None:
                team_member = issues[issue_id]['assigned_to']
            else:
                team_member = pick_random_team_member(team_members, team_uptake_rate)  # Pick a random team member to do this task.
            # In future, we could assign tasks to members based on ability/skillset/time pressures
            random_estimate = issues[issue_id]['estimates'][team_member]  # Pick a random historic estimate the team member has made
            random_velocity = choice(team_velocities[team_member])  # Pick a random historic velocity this team member has achieved
            predicted_time = random_estimate/float(random_velocity)  # Calculate how long this issue should take
            total += predicted_time  # Add it to the total for this project
        project_total = int(total/num_team_members)  # Divide by number of members. For now, assumes all tasks are parallelisable
        total_estimates.append(project_total)  # Add to list of estimates

    total_estimates.sort()  # Sort, so estimates are in chronological order
    return total_estimates

def get_quartiles(total_estimates, num_simulations):
    q1 = total_estimates[num_simulations/4]  # 25% chance we will finish in this time
    q2 = total_estimates[num_simulations/2]  # 50% chance we will finish in this time
    q3 = total_estimates[3*num_simulations/4]  # 75% chance we will finish in this time
    return q1, q2, q3

def main():
    # Four team members
    # In future, we will see how each member estimates and works in different ways
    team_members = ["anna", "bill", "cass", "dave"]

    num_issues_total = 40
    num_issues_completed = 20

    issues = load_issues_from_file("issues.json")

    team_estimates = calculate_team_member_estimates(team_members, issues)

    team_velocities = calculate_team_velocities(team_members, issues)

    team_uptake_rate = calculate_uptake_rate(team_members, issues)


    # Get a list of ids for completed and incomplete issues
    todo_issue_ids = get_todo_ids(issues)
    done_issue_ids = get_done_ids(issues)

    # How many samples do we want? Using 100 allows us to easily convert into percentages
    num_simulations = 1000

    # A list of estimates for the whole project
    total_estimates = run_monte_carlo_simulation(num_simulations, issues, team_members, team_velocities, team_uptake_rate, todo_issue_ids, done_issue_ids)

    results = get_quartiles(total_estimates, num_simulations)
    print results



if __name__ == '__main__':
    main()