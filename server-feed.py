#run with: python3 server-feed.py
import subprocess
import json
def convert(arr):
    built = ""
    for item in arr:
        built += str(item)
    return built


class Process:
    buffer = []
    open_count = 0
    closed_count = 0

    def process_line(self, line):
        if "StatManagerLog" in line:
            self.open_count = 1
            self.buffer.append("{")
        elif "{" in line:
            self.open_count += 1
            self.buffer.append("{")
        elif "}" in line:
            self.closed_count += 1
            self.buffer.append("}")
            if self.open_count == self.closed_count:
                self.open_count = 0
                self.closed_count = 0
                print(json.loads(convert(self.buffer))) #post request here
                self.buffer.clear()
        else:
            if self.open_count > 0:
                self.buffer.append(line)
parser = Process()

def tail_file(file_path):
    # Use 'tail -n 0 -f' to start from the end of the file and follow updates
    tail_command = ['tail', '-n', '0', '-f', file_path]

    try:
        # Open a subprocess to run the tail command
        with subprocess.Popen(tail_command, stdout=subprocess.PIPE, text=True) as process:
            # Process the output line by line
            for line in process.stdout:
                # Strip newline character and process the line
                parser.process_line(line.strip())
    except KeyboardInterrupt:
        print("Script terminated by user.")

# Replace 'your_log_file.log' with the actual path to your log file
log_file_path = 'pavlovserver/Pavlov/Saved/Logs/Pavlov.log'
try:
    tail_file(log_file_path)
except Exception as e:
    print(f"Error: {e}")
