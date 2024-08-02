#!/bin/bash

# Get the current working directory where the bash script is located
current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Current directory: $current_dir"

# Directory where the input and output files are located (same as the working directory)
input_output_dir="$current_dir"
echo "Input/Output directory: $input_output_dir"

# Path to your scheduler-gpt.py script (assuming it's in the same directory)
scheduler_script="$current_dir/scheduler-gpt.py"
echo "Scheduler script path: $scheduler_script"

# List all .in files in the directory
input_files=("$input_output_dir"/*.in)

for input_file in "${input_files[@]}"; do
    filename=$(basename -- "$input_file")
    output_file="${filename%.*}.out"
    expected_output_path="$input_output_dir/$output_file"

    echo "Processing test for $filename"

    # Run the scheduler-gpt.py script with the input file
    python "$scheduler_script" "$input_file"

    # Check if the generated output matches the expected output
    generated_output_path="$input_output_dir/$output_file"
    if cmp -s "$generated_output_path" "$expected_output_path"; then
        echo "Test for $filename passed"
    else
        echo "Test for $filename failed"
    fi
done
