# run with: python3 server-feed.py
import subprocess
import json

import requests

PROD = True


def convert(arr):
    built = ""
    for item in arr:
        built += str(item)
    return built


buffer = []
open_count = 0
closed_count = 0
logging = False


def process_line(line):
    global open_count, closed_count, buffer, logging
    if "StatManagerLog" in line and "Dumping Stats" not in line:
        logging = True
        open_count = 1
        buffer.append("{")
    elif "{" in line and logging:
        open_count += 1
        buffer.append("{")
    elif "}" in line and logging:
        closed_count += 1
        buffer.append("}")
        if open_count == closed_count:
            open_count = 0
            closed_count = 0
            logging = False
            try:
                data = json.loads(convert(buffer))
            except json.decoder.JSONDecodeError:
                data = json.loads(convert(buffer[1:]))
            print(data)
            if PROD:
                if "KillData" in data:
                    requests.post("https://shackmm.com/NAE-ONE/kill", data=json.dumps(data),
                                  headers={"Content-Type": "application/json", "key": "pvE4VgbvLZXbwoew8mYi"})
                elif "RoundEnd" in data:
                    requests.post("https://shackmm.com/NAE-ONE/end", data=json.dumps(data),
                                  headers={"Content-Type": "application/json", "key": "pvE4VgbvLZXbwoew8mYi"})
                elif "RoundState" in data:
                    requests.post("https://shackmm.com/NAE-ONE/state", data=json.dumps(data),
                                  headers={"Content-Type": "application/json", "key": "pvE4VgbvLZXbwoew8mYi"})
                elif "BombData" in data:
                    requests.post("https://shackmm.com/NAE-ONE/bomb", data=json.dumps(data),
                                  headers={"Content-Type": "application/json", "key": "pvE4VgbvLZXbwoew8mYi"})
            buffer.clear()
    else:
        if open_count > 0:
            buffer.append(line)


def tail_file(file_path):
    # Use 'tail -n 0 -f' to start from the end of the file and follow updates
    tail_command = ['tail', '-n', '0', '-f', file_path]

    try:
        # Open a subprocess to run the tail command
        with subprocess.Popen(tail_command, stdout=subprocess.PIPE, text=True) as process:
            # Process the output line by line
            for line in process.stdout:
                # Strip newline character and process the line
                process_line(line.strip())
    except KeyboardInterrupt:
        print("Script terminated by user.")


# Replace 'your_log_file.log' with the actual path to your log file
log_file_path = 'pavlovserver/Pavlov/Saved/Logs/Pavlov.log'
try:
    tail_file(log_file_path)
except Exception as e:
    print(buffer)
    print(f"Error: {e}")
