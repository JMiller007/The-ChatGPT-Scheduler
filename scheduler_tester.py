import os
import subprocess
import filecmp
import threading

# Get the current working directory where this Python script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Directory where the input and output files are located (same as the working directory)
input_output_dir = current_dir

# Path to your scheduler-gpt.py script (assuming it's in the same directory)
scheduler_script = os.path.join(current_dir, "scheduler-gpt.py")

# List all .in files in the directory
input_files = [f for f in os.listdir(input_output_dir) if f.endswith(".in")]

def run_scheduler(input_file, expected_output_path):
    filename = os.path.basename(input_file)
    output_file = os.path.splitext(filename)[0] + ".out"
    generated_output_path = os.path.join(input_output_dir, output_file)

    # Run the scheduler-gpt.py script with the input file, add a timeout of 30 seconds
    try:
        subprocess.run(["python", scheduler_script, input_file], cwd=input_output_dir, timeout=30)
    except subprocess.TimeoutExpired:
        print(f"Test for {filename} timed out")
        return

    # Check if the generated output matches the expected output
    if filecmp.cmp(generated_output_path, expected_output_path, shallow=False):
        print(f"Test for {filename} passed")
    else:
        print(f"Test for {filename} failed")

# Create a list to store threads for running scheduler tests
threads = []

for input_file in input_files:
    filename = os.path.basename(input_file)
    output_file = os.path.splitext(filename)[0] + ".out"
    expected_output_path = os.path.join(input_output_dir, output_file)

    # Create a thread for each test
    thread = threading.Thread(target=run_scheduler, args=(input_file, expected_output_path))
    threads.append(thread)

# Start all threads
for thread in threads:
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()
