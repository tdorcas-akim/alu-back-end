#!/usr/bin/python3
"""Exports all employees' todo list information to JSON format"""

import json
import requests

if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/users"
    users = requests.get(url).json()

    all_tasks = {}

    for user in users:
        user_id = user.get("id")
        username = user.get("username")
        todos_url = f"https://jsonplaceholder.typicode.com/todos?userId=
        {user_id}"
        todos = requests.get(todos_url).json()

        task_list = []
        for task in todos:
            task_info = {
                "username": username,
                "task": task.get("title"),
                "completed": task.get("completed")
            }
            task_list.append(task_info)

        all_tasks[user_id] = task_list

    with open("todo_all_employees.json", "w") as f:
        json.dump(all_tasks, f)
