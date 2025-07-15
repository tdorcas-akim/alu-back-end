#!/usr/bin/python3
"""
This script gets data from a fake online API for a specific employee ID,
and saves all their tasks into a JSON file.
"""


import json
import requests
import sys

if __name__ == "__main__":
    # First, make sure the user gave us one argument (the employee ID)
    if len(sys.argv) != 2:
        print("Usage: {} <employee_id>".format(sys.argv[0]))
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
        # Try converting the ID to an integer
    except ValueError:
        print("Employee ID must be an integer")
        sys.exit(1)

    # This is the base URL where the fake API lives
    base_url = "https://jsonplaceholder.typicode.com"

    try:
        # We want to get the employee's username first
        user_url = "{}/users/{}".format(base_url, employee_id)
        user_response = requests.get(user_url)
        user_response.raise_for_status(
        # This checks if the request worked
        user_data = user_response.json()

        username = user_data.get("username")
        # Get the username from the response
        if not username:
            print("User not found.")
            sys.exit(1)

        # Now let's get their todo tasks
        todos_url = "{}/todos?userId={}".format(base_url, employee_id)
        todos_response = requests.get(todos_url)
        todos_response.raise_for_status()
        todos_data = todos_response.json()

        # Let's build the structure expected in the JSON file
        task_list = []
        for task in todos_data:
            # We create a dictionary for each task with only what we need
            task_info = {
                "task": task.get("title"),
                "completed": task.get("completed"),
                "username": username
            }
            task_list.append(task_info)

        # The final JSON structure is like: {"2": [task1, task2, ...]}
        final_data = {str(employee_id): task_list}

        # Save to a JSON file named like: 2.json
        filename = "{}.json".format(employee_id)
        with open(filename, "w") as json_file:
            json.dump(final_data, json_file)

    except requests.exceptions.RequestException as e:
        print("Error with network or request:", e)
        sys.exit(1)

    except ValueError:
        print("Error decoding JSON response")
        sys.exit(1)

    except IOError as e:
        print("Error writing to file:", e)
        sys.exit(1)
