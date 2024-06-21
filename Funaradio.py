import requests
import sys
import base64

args = sys.argv

if len(args) < 2: print("Please enter an argument") ; exit(1)

if args[1] == "set":
    if len(args) < 3: print("Please enter new token") ; exit(1)
    with open("github-token.txt", "w") as file:
        file.write(args[2])
    exit(0)

if args[1] == "create":
    print("Comming soon")
    exit(0)

if args[1] == "upload":
    if len(args) < 3: print("Please enter file path") ; exit(1)
    file_path = args[2]

    with open("github-token.txt", "r") as file:
        token = file.readlines()[0]

    # Read the file content and encode it as base64
    with open(file_path, 'rb') as file:
        file_content = file.read()
        base64_content = base64.b64encode(file_content).decode('utf-8')

    # Get current file details to obtain the SHA
    response = requests.get('https://api.github.com/repos/Bugxit/Funaradio/contents/docs/news.png', headers={'Authorization': f'token {token}'})

    # Check the response
    if response.status_code == 200:
        file_info = response.json()
        current_sha = file_info['sha']

        data = {
            'message': "Update news.png using Python API",
            'content': base64_content,
            'sha': current_sha,
            'branch': 'main'
        }

        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        response = requests.put('https://api.github.com/repos/Bugxit/Funaradio/contents/docs/news.png', headers=headers, json=data)

        # Check the response
        if response.status_code == 200:
            print('File updated successfully.')
        else:
            print(f'Failed to update file. Status code: {response.status_code}')
            print(response.json())
    else:
        print(f'Failed to retrieve current file details. Status code: {response.status_code}')
        print(response.json())
