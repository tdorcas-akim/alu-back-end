#!/usr/bin/python3
"""
This script fetches data from a REST API for a given employee ID and
exports all of their tasks to a CSV file.
"""


import csv
import requests
import sys

if __name__ == "__main__":
    # --- Step 1: Get and Validate the Employee ID ---
    # The script should be called with exactly one argument: the employee ID.
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: {} <employee_id>\n".format(sys.argv[0]))
        sys.exit(1)

<<<<<<< HEAD
    # We'll try to convert the argument to an integer.
=======
    # We'll try to convert the argument to an integer. 
>>>>>>> 7c3200832ca01f27ca20130da2aedcb250bb0030
    # If it fails, it's bad input.
    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        sys.stderr.write("Employee ID must be an integer\n")
        sys.exit(1)

    # --- Step 2: Fetch Data from the API ---
    # We need both the employee's username and their list of tasks.
    base_url = "https://jsonplaceholder.typicode.com"
    try:
        # First, get the user's details to find their username.
        user_url = "{}/users/{}".format(base_url, employee_id)
        user_response = requests.get(user_url)
        user_response.raise_for_status()  # This will fail on a 404 Not Found
        user_data = user_response.json()
        username = user_data.get('username')

        if not username:
            sys.stderr.write("User with ID {} not found\n".format(employee_id))
            sys.exit(1)

        # Next, get all the to-do items for this user.
        todos_url = "{}/todos".format(base_url)
        params = {"userId": employee_id}
        todos_response = requests.get(todos_url, params=params)
        todos_response.raise_for_status()
        todos_data = todos_response.json()

    except requests.exceptions.RequestException as e:
        # This catches network errors, timeouts, bad URLs, etc.
        sys.stderr.write("Error communicating with API: {}\n".format(e))
        sys.exit(1)
    except ValueError:
        # This catches errors if the API response isn't valid JSON.
        sys.stderr.write("Error decoding API response\n")
        sys.exit(1)

    # --- Step 3: Write the Data to a CSV File ---
    # The filename is just the employee's ID with a .csv extension.
    csv_filename = "{}.csv".format(employee_id)

    try:
        # We open the file with 'with' so it's automatically closed.
        # newline='' is important to prevent extra blank rows in the CSV.
        with open(csv_filename, mode='w', newline='') as csv_file:
            # The writer object does the work of formatting the CSV.
            # We use QUOTE_ALL to make sure every field is in double quotes.
            writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

            # We go through each task and write one row for it in the CSV.
            for task in todos_data:
                writer.writerow([
                    employee_id,
                    username,
                    task.get('completed'),
                    task.get('title')
                ])
    except IOError as e:
        sys.stderr.write("Error writing to file {}: {}\n".format(
            csv_filename, e))
        sys.exit(1)
