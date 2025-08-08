# imports
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pytz import timezone

# Configuration
SCRIPT_MONITOR_NAME = "YFOD Script Monitor"
SCRIPT_MONITOR_VERSION = "1.0"
LOG_DIR = "logs"
SCRIPT_DIR = "scripts"

# Get current time
def get_current_time():
    tz = timezone('US/Eastern')
    current_time = datetime.now(tz)
    return current_time.strftime("%Y-%m-%d %H:%M:%S")

# Create log directory if it doesn't exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Create script directory if it doesn't exist
if not os.path.exists(SCRIPT_DIR):
    os.makedirs(SCRIPT_DIR)

# Load scripts from script directory
def load_scripts():
    scripts = []
    for filename in os.listdir(SCRIPT_DIR):
        if filename.endswith(".py"):
            scripts.append(filename)
    return scripts

# Run script and log results
def run_script(script_name):
    start_time = get_current_time()
    try:
        exec(open(os.path.join(SCRIPT_DIR, script_name)).read())
        result = "Success"
    except Exception as e:
        result = "Error: " + str(e)
    end_time = get_current_time()
    log_results(script_name, start_time, end_time, result)

# Log results to file
def log_results(script_name, start_time, end_time, result):
    log_file = os.path.join(LOG_DIR, "script_monitor.log")
    with open(log_file, "a") as f:
        f.write(f"{script_name},{start_time},{end_time},{result}\n")

# Print script monitor header
print(f"{SCRIPT_MONITOR_NAME} v{SCRIPT_MONITOR_VERSION}")
print("-------------------------------------------------")

# Load and run scripts
scripts = load_scripts()
for script in scripts:
    print(f"Running script: {script}")
    run_script(script)
    print(f"Script {script} completed.\n")

# Generate log report
log_data = pd.read_csv(os.path.join(LOG_DIR, "script_monitor.log"), header=None, names=["Script", "Start Time", "End Time", "Result"])
print("Script Monitor Log Report:")
print("-------------------------------")
print(log_data)

# Generate log graph
log_data.plot(x="Start Time", y="End Time", kind="line")
plt.title("Script Monitoring Graph")
plt.xlabel("Start Time")
plt.ylabel("End Time")
plt.show()