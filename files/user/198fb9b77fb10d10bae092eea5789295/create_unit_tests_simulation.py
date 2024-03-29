# filename: create_unit_tests_simulation.py
import os
import requests
import time
import json

def check_task_status(base_url, task_id):
    check_url = f'{base_url}check-status/{task_id}'
    while True:
        response = requests.get(check_url)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'completed':
                return data
            elif data.get('status') == 'error':
                print(f"Error processing task {task_id}: {data.get('message')}")
                return None
        else:
            print(f"Failed to check task status. Status code: {response.status_code}")
            return None
        print(f"Task {task_id} is still processing. Checking again in 10 seconds...")
        time.sleep(10)

def create_unit_tests_simulation(parent_dir, base_url):
    uut_dir = 'UUT'
    uut_path = os.path.join(parent_dir, uut_dir)

    if not os.path.exists(uut_path):
        print(f"Directory '{uut_path}' does not exist.")
        return

    request_url = f'{base_url}process-files'

    for file_name in os.listdir(uut_path):
        if file_name.endswith('.cpp'):
            cpp_file_path = os.path.join(uut_path, file_name)
            with open(cpp_file_path, 'r') as cpp_file:
                cpp_file_content = cpp_file.read()
                json_payload = {'cppFileContent': cpp_file_content}
                response = requests.post(request_url, json=json_payload)

                if response.status_code == 200:
                    data = response.json()
                    if data.get('status') == 'processing':
                        print(f"Processing started for {file_name}. Task ID: {data.get('id')}")
                        task_result = check_task_status(base_url, data.get('id'))
                        if task_result:
                            print(f"Task completed. Results: {task_result}")
                    else:
                        print(f"Error: {data.get('message')}")
                else:
                    print(f"Failed to submit files. Status code: {response.status_code}")

# Set the parent directory where the UUT directory is located
parent_dir = '/home/wilsonb/dl/github.com/BruceRayWilson/Accounting'
# Set the base URL of your web server
base_url = 'http://127.0.0.1:5000/'

create_unit_tests_simulation(parent_dir, base_url)