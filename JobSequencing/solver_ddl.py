import math
import Task
from parse import read_input_file, write_output_file
import os

def get_total_time(sequence, tasks):
    time = 0
    for i in sequence:
        time += tasks[i-1].get_duration()
    return time


def check_for_lateness(sequence, tasks, new_job):
    new_deadline = tasks[new_job - 1].get_deadline()
    new_time = tasks[new_job-1].get_duration()
    back = len(sequence)-1
    while back >= 0:
        this_deadline = tasks[sequence[back]-1].get_deadline()
        if get_total_time(sequence[:back+1], tasks) + new_time > this_deadline:
            return -1
        elif this_deadline <= new_deadline:
            if get_total_time(sequence[:back + 1], tasks) + new_time < new_deadline:
                return back
        back -= 1
    return back


def sort_by_density(densities, length):
    sorted_densities = []
    for _ in range(length):
        max_density = densities[0]
        for i in range(len(densities)):
            if densities[i][1] > max_density[1]:
                max_density = densities[i]
        sorted_densities.append(max_density)
        densities.remove(max_density)
    return sorted_densities


def get_sequence(time_description):
    job_sequence = []
    finished_jobs = set()
    back_index = 1439
    while back_index >= 0:
        the_job = time_description[back_index]
        if the_job == 0:
            pass
        elif the_job in finished_jobs:
            pass
        else:
            job_sequence.insert(0, the_job)
            finished_jobs.add(the_job)
        back_index -= 1
    return job_sequence


def calculate_profit(id_list, tasks):
    profit = 0
    curr_t = 0
    for i in range(len(id_list)):
        curr_t += tasks[id_list[i] - 1].get_duration()
        if curr_t <= 1440:
            profit += tasks[id_list[i] - 1].get_late_benefit(curr_t - tasks[id_list[i] - 1].get_deadline())
        else:
            break
    return profit


def solve(tasks):
    place_to_put_after = [1/i for i in range(1, 21)]
    job_counts = len(tasks)
    densities = []
    for i in range(job_counts):
        i_plus_1th_density = \
            tasks[i].get_late_benefit(tasks[i].get_duration() - tasks[i].get_deadline()) / tasks[i].get_duration()
        densities.append([i + 1, i_plus_1th_density])
    densities = sort_by_density(densities, job_counts)

    # time_occupation = []
    # time_description = []
    # for i in range(1440):
    #     time_occupation.append(1)
    #     time_description.append(0)

    job_sequence = []
    for i in range(len(densities)):
        this_job_index = densities[i][0]
        this_job = tasks[densities[i][0]-1]
        lateness = check_for_lateness(job_sequence, tasks, this_job_index)
        if len(job_sequence) == 0:
            job_sequence.append(this_job_index)
        elif lateness != -1:
            job_sequence.insert(lateness + 1, this_job_index)
        else:
            max_profit = calculate_profit(job_sequence, tasks)
            best_sequence = job_sequence.copy()
            swapped_task = -1
            swapped_index = -1

            for j in range(len(job_sequence)):
                compared_job = job_sequence[j]
                current_sequence = job_sequence.copy()
                current_sequence.remove(compared_job)
                current_sequence.insert(j, densities[i][0])
                updated_profit = calculate_profit(current_sequence, tasks)

                if updated_profit > max_profit:
                    best_sequence = current_sequence
                    max_profit = updated_profit
                    swapped_task = compared_job
                    swapped_index = j

            if swapped_index != -1:
                best_sequence_copy = best_sequence.copy()

                potential_sequence = best_sequence.copy()
                potential_sequence.insert(0, swapped_task)

                best_profit = calculate_profit(potential_sequence, tasks)
                best_sequence = potential_sequence

                for k in place_to_put_after:
                    current_sequence = best_sequence_copy.copy()

                    index_to_put = int(k * len(current_sequence))
                    # current_sequence.insert(index_to_put, swapped_task)
                    # current_profit = calculate_profit(current_sequence, tasks)
                    # if current_profit > best_profit:
                    #     best_sequence = current_sequence
                    #     best_profit = current_profit

                    new_swapped_one = current_sequence.pop(index_to_put-1)
                    current_sequence.insert(index_to_put, swapped_task)
                    current_sequence.append(new_swapped_one)

                    current_profit = calculate_profit(current_sequence, tasks)
                    if current_profit > best_profit:
                        best_sequence = current_sequence
                        best_profit = current_profit

            else:
                best_sequence.append(densities[i][0])

            job_sequence = best_sequence

    return job_sequence


def sanity_checker(sequence):
    total_time = 0
    seen = set()
    duplicate = []
    for job_index in sequence:
        if job_index in seen:
            print("Error")
            duplicate.append(job_index)
        seen.add(job_index)
        total_time += tasks[job_index - 1].get_duration()
    print(total_time)


tasks = read_input_file("small/small-2.in")
final_sequence = solve(tasks)
sanity_checker(final_sequence)
print(calculate_profit(final_sequence, tasks))
print(final_sequence)