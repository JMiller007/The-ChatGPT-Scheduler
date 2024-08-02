# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 19:33:08 2023

@author: brand
"""

import sys
import heapq


class Process:
    def __init__(self, name, arrival_time, burst_time, weight):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.status = "arrived"
        self.start_time = None
        self.finish_time = None
        self.virtual_runtime = 0
        self.weight = weight
        self.remaining_time = burst_time
        self.printed_arrival = False


def cfs_scheduling(processes, run_time):
    current_time = 0
    waiting_time = 0
    turnaround_time = 0

    events = []

    while current_time < run_time:
        runnable_processes = [process for process in processes if
                              process.arrival_time <= current_time and process.status == "arrived"]

        if not runnable_processes:
            events.append(f"Time {current_time} : Idle")
            current_time += 1
        else:
            # Select the process with the smallest virtual runtime
            shortest_runtime_process = min(runnable_processes, key=lambda x: x.virtual_runtime)
            shortest_runtime_process.status = "selected"
            events.append(f"Time {current_time} : {shortest_runtime_process.name} arrived")
            events.append(
                f"Time {current_time} : {shortest_runtime_process.name} selected (burst {shortest_runtime_process.burst_time})")
            waiting_time += current_time - shortest_runtime_process.arrival_time
            shortest_runtime_process.start_time = current_time
            current_time += shortest_runtime_process.burst_time
            turnaround_time += current_time - shortest_runtime_process.arrival_time
            shortest_runtime_process.finish_time = current_time
            shortest_runtime_process.status = "finished"
            events.append(f"Time {current_time} : {shortest_runtime_process.name} finished")

            # Update the virtual runtime of all runnable processes
            for process in runnable_processes:
                process.virtual_runtime += (current_time - process.arrival_time) / process.weight

    avg_waiting_time = waiting_time / len(processes)
    avg_turnaround_time = turnaround_time / len(processes)

    events.append(f"Finished at time {current_time}")

    return avg_waiting_time, avg_turnaround_time, events


def preemptive_sjf_scheduling(processes, run_time):
    current_time = 0
    waiting_time = 0
    turnaround_time = 0
    process_heap = []  # Min-heap to track processes by remaining burst time
    events = []

    old_process = None

    while current_time < run_time or process_heap:
        # Add arriving processes to the min-heap
        for process in processes:
            if process.arrival_time <= current_time and process.status == "arrived" and process.remaining_time > 0:
                events.append(f"Time {current_time} : {process.name} arrived")
                process.status = "selected"
                heapq.heappush(process_heap, (process.remaining_time, process.name, process))

        if not process_heap:
            events.append(f"Time {current_time} : Idle")
            current_time += 1
            continue

        # Select the process with the shortest remaining burst time
        shortest_time, _, current_process = heapq.heappop(process_heap)

        # checks if selected needs to be printed again
        if current_process.start_time is None or current_process != old_process:
            events.append(
                f"Time {current_time} : {current_process.name} selected (burst {current_process.remaining_time})")

        if current_process.start_time is None:
            current_process.start_time = current_time

        current_time += 1
        current_process.remaining_time -= 1

        old_process = current_process

        for new_process in processes:
            if new_process.arrival_time <= current_time and new_process.status == "arrived" and new_process.remaining_time > 0:
                events.append(f"Time {current_time} : {new_process.name} arrived")
                new_process.status = "selected"
                heapq.heappush(process_heap, (new_process.remaining_time, new_process.name, new_process))

        if current_process.remaining_time == 0:
            current_process.finish_time = current_time
            current_process.status = "finished"
            events.append(f"Time {current_time} : {current_process.name} finished")

        else:
            heapq.heappush(process_heap, (shortest_time - 1, current_process.name, current_process))

    avg_waiting_time = waiting_time / len(processes)
    for process in processes:
        turnaround_time += process.finish_time - process.arrival_time

    avg_turnaround_time = turnaround_time / len(processes)

    events.append(f"Finished at time {current_time}")

    return avg_waiting_time, avg_turnaround_time, events


def sjf_scheduling(processes, run_time):
    current_time = 0
    waiting_time = 0
    turnaround_time = 0

    events = []

    while current_time < run_time:
        runnable_processes = [process for process in processes if
                              process.arrival_time <= current_time and process.status == "arrived"]

        if not runnable_processes:
            events.append(f"Time {current_time} : Idle")
            current_time += 1
        else:
            # Select the shortest job from all runnable processes
            shortest_job = min(runnable_processes, key=lambda x: x.burst_time)
            shortest_job.status = "selected"
            if shortest_job.printed_arrival == False:
                events.append(f"Time {current_time} : {shortest_job.name} arrived")
            events.append(f"Time {current_time} : {shortest_job.name} selected (burst {shortest_job.burst_time})")
            waiting_time += current_time - shortest_job.arrival_time
            shortest_job.start_time = current_time
            old_curr_time = current_time
            current_time += shortest_job.burst_time

            print(f"for loop from {old_curr_time} to {current_time + 1}")
            # checking for processes that have arrived during the burst time of another process
            for i in range(current_time - shortest_job.burst_time, current_time + 1):
                print("i is ", i)
                for process in processes:
                    print("in second loop")
                    if process.arrival_time == i and process.status != "selected":
                        print("in if statement with ", process.name)
                        events.append(f"Time {i} : {process.name} arrived")
                        process.printed_arrival = True

            turnaround_time += current_time - shortest_job.arrival_time
            shortest_job.finish_time = current_time
            shortest_job.status = "finished"
            events.append(f"Time {current_time} : {shortest_job.name} finished")

    avg_waiting_time = waiting_time / len(processes)
    avg_turnaround_time = turnaround_time / len(processes)

    events.append(f"Finished at time {current_time}")

    return avg_waiting_time, avg_turnaround_time, events


def fcfs_scheduling(processes, run_time):
    sorted_processes = sorted(processes, key=lambda x: x.arrival_time)

    current_time = 0
    waiting_time = 0
    turnaround_time = 0

    events = []

    while current_time < run_time:
        runnable_processes = [process for process in sorted_processes if
                              process.arrival_time <= current_time and process.status == "arrived"]

        if not runnable_processes:
            events.append(f"Time {current_time} : Idle")
            current_time += 1
        else:
            process = runnable_processes[0]
            process.status = "selected"
            events.append(f"Time {current_time} : {process.name} arrived")
            events.append(f"Time {current_time} : {process.name} selected (burst {process.burst_time})")
            waiting_time += current_time - process.arrival_time
            process.start_time = current_time
            current_time += process.burst_time
            turnaround_time += current_time - process.arrival_time
            process.finish_time = current_time
            process.status = "finished"

    avg_waiting_time = waiting_time / len(sorted_processes)
    avg_turnaround_time = turnaround_time / len(sorted_processes)

    events.append(f"Finished at time {current_time}")

    return avg_waiting_time, avg_turnaround_time, events


def round_robin_scheduling(processes, run_time, quantum):
    current_time = 0
    waiting_time = 0
    turnaround_time = 0
    remaining_time = [process.burst_time for process in processes]
    queue = []

    events = []

    events.append(f"Quantum   {quantum}\n\n")

    # print("Run time:",run_time,"\n Quantum is", quantum)

    while current_time < run_time or queue:
        # Add arriving processes to the queue
        for i, process in enumerate(processes):
            if process.arrival_time <= current_time and process.status == "arrived" and remaining_time[i] > 0:
                queue.append(i)
                # print("Appending process ", i, "in beginning")
                process.status = "selected"
                events.append(f"Time {process.arrival_time} : {process.name} arrived")

        if not queue:
            events.append(f"Time {current_time} : Idle")
            current_time += 1
            # print("In not queue at time ", current_time)

        else:
            # print("\n\ncurrent time is ", current_time)
            # print(queue)
            process_index = queue.pop(0)
            process = processes[process_index]
            # print("selected process is ", process.name)

            # figure out how big the time slice will be
            if remaining_time[process_index] <= quantum:
                time_slice = remaining_time[process_index]
            else:
                time_slice = quantum
            # record the start time of the process
            if process.start_time is None:
                process.start_time = current_time

            events.append(f"Time {current_time} : {process.name} selected (burst {remaining_time[process_index]})")

            waiting_time += current_time - process.arrival_time

            current_time += time_slice
            # print("current time is ", current_time)
            remaining_time[process_index] -= time_slice

            # check for processes that have arrived while another was running (human code)
            for i, item in enumerate(processes):
                if i == process_index:
                    continue
                if item.arrival_time <= current_time and item.status != "selected" and item.status != "queued" and item.arrival_time >= (
                        current_time - quantum):
                    events.append(f"Time {item.arrival_time} : {item.name} arrived")
                    item.status = "queued"
                    queue.append(i)
                # print("Appended process ",i)

            if remaining_time[process_index] == 0:
                # print("Assigning finish time for ",process.name)
                process.finish_time = current_time
                process.status = "finished"
                events.append(f"Time {current_time} : {process.name} finished")
            else:
                queue.append(process_index)
                # print("Appending at end")

            # print("Last queue is\n",queue)

    avg_waiting_time = waiting_time / len(processes)
    for process in processes:
        turnaround_time += process.finish_time - process.arrival_time

    avg_turnaround_time = turnaround_time / len(processes)

    events.append(f"Finished at time {current_time}")

    return avg_waiting_time, avg_turnaround_time, events


def calculate_metrics(processes):
    for process in processes:
        # print("Process name is ",process.name)
        # print("finish time is ", process.finish_time, "arrival time is ", process.arrival_time)
        process.turnaround_time = process.finish_time - process.arrival_time
        # print("Process finish time is ", process.finish_time, " and arrived at ", process.arrival_time)
        process.waiting_time = process.turnaround_time - process.burst_time
        process.response_time = process.start_time - process.arrival_time


def display_events(events):
    for event in events:
        print(event)


def main():
    # print(len(sys.argv)) replaces in file
    if len(sys.argv) != 2:
        print("Usage: python scheduling.py input_file.in")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
            process_count = None
            run_time = None
            scheduling_algorithm = None
            quantum = None

            processes = []

            for line in lines:
                line = line.strip()
                if line.startswith('#') or len(line) == 0:
                    continue  # Skip comments and empty lines
                parts = line.split()
                keyword = parts[0].lower()
                if keyword == "processcount":
                    process_count = int(parts[1])
                elif keyword == "runfor":
                    run_time = int(parts[1])
                elif keyword == "use":
                    scheduling_algorithm = parts[1]
                elif keyword == "quantum":
                    quantum = int(parts[1])
                elif keyword == "process":
                    name = parts[2]
                    arrival_time = int(parts[4])
                    burst_time = int(parts[6])

                    if "with" in parts and scheduling_algorithm.lower() == "cfs":
                        weight_index = parts.index("with") + 2
                        weight = int(parts[weight_index])
                    else:
                        weight = 0

                    processes.append(Process(name, arrival_time, burst_time, weight))

                elif keyword == "end":
                    break

        if process_count is None or run_time is None or scheduling_algorithm is None:
            print("Invalid input file format. Make sure it specifies processcount, runfor, and use.")
            sys.exit(1)

        print(input_file.replace(".in", ".out"))
        # maybe change this to just do an output file and not use replace
        with open(input_file.replace(".in", ".out"), 'w') as output_file:
            output_file.write(f"{process_count} processes\n")

            # human code (Kirk) begin
            if (scheduling_algorithm == "sjf"):
                algo = str("preemptive Shortest Job First")
            elif (scheduling_algorithm == "rr"):
                algo = str("Round Robin")
            elif (scheduling_algorithm == "fcfs"):
                algo = str("First Come First Serve")
            output_file.write(f"Using {algo}")
            # human code (Kirk) end
            # output_file.write(f"Using {scheduling_algorithm}")
            if scheduling_algorithm.lower() == "roundrobin" and quantum is not None:
                output_file.write(f"\nQuantum {quantum}\n")
            else:
                output_file.write("\n")

            if scheduling_algorithm.lower() == "fcfs":
                avg_waiting_time, avg_turnaround_time, events = fcfs_scheduling(processes, run_time)
                # output_file.write("FCFS Scheduling Events:\n")
                for event in events:
                    output_file.write(event + '\n')
            elif scheduling_algorithm.lower() == "sjf":
                avg_waiting_time, avg_turnaround_time, events = preemptive_sjf_scheduling(processes, run_time)
                # output_file.write("SJF Scheduling Events:\n")
                for event in events:
                    output_file.write(event + '\n')
            elif scheduling_algorithm.lower() == "rr":
                avg_waiting_time, avg_turnaround_time, events = round_robin_scheduling(processes, run_time, quantum)
                # output_file.write("Round Robin Scheduling Events:\n")
                for event in events:
                    output_file.write(event + '\n')
            elif scheduling_algorithm.lower() == "cfs":
                avg_waiting_time, avg_turnaround_time, events = cfs_scheduling(processes, run_time)
                # output_file.write("CFS Scheduling Events:\n")
                for event in events:
                    output_file.write(event + '\n')
            else:
                print(f"Unsupported scheduling algorithm: {scheduling_algorithm}")
                sys.exit(1)

            calculate_metrics(processes)

            # output_file.write("\nScheduling Metrics:")
            output_file.write("\n")
            for process in processes:
                output_file.write(
                    f"{process.name} wait {process.waiting_time} turnaround {process.turnaround_time} response {process.response_time}\n")
            # output_file.write(f"Average Turnaround Time: {avg_turnaround_time}\n")
            # output_file.write(f"Average Waiting Time: {avg_waiting_time}\n")

            # Check for unfinished processes
            unfinished_processes = [process for process in processes if process.status != "finished"]
            if unfinished_processes:
                output_file.write("\nUnfinished Processes:\n")
                for process in unfinished_processes:
                    output_file.write(f"{process.name} did not finish\n")

        print(f"Results written to {input_file.replace('in', 'out')}")

    except FileNotFoundError:
        print(f"File not found: {input_file}")
        sys.exit(1)


if __name__ == "__main__":
    main()