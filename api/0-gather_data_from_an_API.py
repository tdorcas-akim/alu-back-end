#!/usr/bin/python3
"""
A simple Python script that, for a given employee ID,
returns information about his/her TODO list progress.
"""

import requests
import sys


if __name__ == "__main__":
    # Check if the user provided an employee ID
    if len(sys.argv) != 2:
        print("Usage: python3 0-gather_data_from_an_API.py <employee_id>")
        sys.exit(1)

    # Try to convert the argument to an integer
    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("Error: Employee ID must be an integer.")
        sys.exit(1)

    # Base URL for the API
    base_url = "https://jsonplaceholder.typicode.com/"
    # --- Step 1: Get Employee Information ---
    # We will send a request to get the user's details, like their name"
    # The URL wil be like: https://jsonplaceholder.typicode.com/users/2"
    user_url = base_url + "users/" + str(employee_id)

    # We make the request to get the user's information
    try:
        user_response = requests.get(user_url)
        # This will raise an error if the reuest failed (like 404 Not Found)
        user_response.raise_for_status()
        user_data = user_response.json()
        employee_name = user_data.get("name")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user data: {e}")
        sys.exit(1)
    except ValueError:
        print("Error: Could not decode user JSON response.")
        sys.exit(1)
    # --- Step 2: Get Employee's TODO List ---
    # Now, let's get all the tasks for this employee.
    # The API lets us filter todos by userID.
    # The URL will be:  "https://.../todos?userId=2"
    todos_url = base_url + "todos"
    # We pass the employee ID as a parameter in the URL
    query_params = {"userId": employee_id}

    # We make the request to get the TODO list
    try:
        todos_response = requests.get(todos_url, params=query_params)
        todos_response.raise_for_status()
        todos_data = todos_response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching TODO list: {e}")
        sys.exit(1)
    except ValueError:
        print("Error: Could not decode TODO JSON response.")
        sys.exit(1)
    # --- Step 3: Process the TODO list ---
    # We need to count how many tasks are done and what their titles are.
    completed_tasks = []
    total_tasks = 0

    # We loop through each task in the TODO list we got from the API.
    for task in todos_data:
        total_tasks += 1
        # We check if the 'completed' key has a value of True
        if task.get("completed"):
            # If it's completed, we add its title to our list
            completed_tasks.append(task.get("title"))

    number_of_done_tasks = len(completed_tasks)
    # --- Step 4: Display the Result ---
    # We check if we found an employee name before printing
    if employee_name:
        # First, print the summary line
        print("Employee {} is done with tasks({}/{}):".format(
            employee_name, number_of_done_tasks, total_tasks))

        # Then, loop through the completed tasks and print each one
        for task_title in completed_tasks:
            # Each task title is preceded by a tab and a space
            print("\t {}".format(task_title))
