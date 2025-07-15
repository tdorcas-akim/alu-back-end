#!/usr/bin/python3
"""
This script fetches data from a REST API for a given employee ID and
exports all of their tasks to a CSV file.
"""

import csv
import requests
import sys

if __name__ == "__main__":
    # Base URL for the API we are getting data from.
    base_url = "https://jsonplaceholder.typicode.com/"

    # --- Step 1: Get and Validate the Employee ID ---
    # We need to make sure the user ran the script with a number.
    if len(sys.argv) < 2:
        print("Usage: {} <employee_id>".format(sys.argv[0]))
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("Employee ID must be an integer.")
        sys.exit(1)

    # --- Step 2: Fetch Employee Details ---
    # We need the employee's username for the CSV file.
    # The URL looks like: https://jsonplaceholder.typicode.com/users/2
    user_url = base_url + "users/{}".format(employee_id)
    try:
        user_response = requests.get(user_url)
        user_response.raise_for_status()  # Check for HTTP errors like 404
        user_data = user_response.json()
        username = user_data.get("username")
    except requests.exceptions.RequestException as e:
        print("Error fetching user data: {}".format(e))
        sys.exit(1)
    except ValueError:
        print("Could not decode JSON from user response.")
        sys.exit(1)

    if not username:
        print("Could not find user with ID {}".format(employee_id))
        sys.exit(1)

    # --- Step 3: Fetch the Employee's To-Do List ---
    # This gets all tasks, both completed and not completed.
    # The URL looks like: https://jsonplaceholder.typicode.com/todos?userId=2
    todos_url = base_url + "todos"
    query_params = {"userId": employee_id}
    try:
        todos_response = requests.get(todos_url, params=query_params)
        todos_response.raise_for_status()
        todos_data = todos_response.json()
    except requests.exceptions.RequestException as e:
        print("Error fetching TODO list: {}".format(e))
        sys.exit(1)
    except ValueError:
        print("Could not decode JSON from TODOs response.")
        sys.exit(1)

    # --- Step 4: Write the Data to a CSV File ---
    # The filename will be the employee's ID, like "2.csv".
    csv_filename = "{}.csv".format(employee_id)

    # We use 'with open' because it safely handles closing the file for us.
    with open(csv_filename, mode='w', newline='') as csv_file:
        # Create a writer object that will do the work of writing rows.
        # quoting=csv.QUOTE_ALL makes sure all fields are wrapped in ""
        csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

        # Now, we go through each task we fetched.
        for task in todos_data:
            # We create a list with the exact data needed for each row.
            row = [
                employee_id,
                username,
                task.get("completed"),
                task.get("title")
            ]
            # Write this list as a new row in our CSV file.
            csv_writer.writerow(row)

    # There is no need to print anything to the console.
    # The script will just create the file and exit.