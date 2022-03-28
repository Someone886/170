import math
import solver_s
import parse
from parse import read_input_file, write_output_file
import os


def solve(tasks):
    job_counts = len(tasks)

    # Update the profit of jobs with duration > deadline
    # for i in range(job_counts):
    #     if tasks[i].get_duration() > tasks[i].get_deadline():
    #         tasks[i].perfect_benefit = tasks[i].get_late_benefit(tasks[i].duration - tasks[i].deadline)
    #         tasks[i].deadline = tasks[i].get_duration()

    # Sort jobs based on profit / duration
    densities = []
    for i in range(job_counts):
        i_plus_1th_density = \
            tasks[i].get_late_benefit(tasks[i].get_duration() - tasks[i].get_deadline()) / tasks[i].get_duration()
        densities.append([i + 1, i_plus_1th_density])
    sorted_densities = sort_by_density(densities, job_counts)

    time_occupation = []
    time_description = []
    for i in range(1440):
        time_occupation.append(1)
        time_description.append(0)

    for i in range(len(sorted_densities)):
        job_index = sorted_densities[i][0]
        job_density = sorted_densities[i][1]

        index_in_tasks = job_index - 1
        this_job = tasks[index_in_tasks]
        duration = this_job.get_duration()
        ddl = this_job.get_deadline()
        time_left = sum(time_occupation[:ddl])

        lateness = 0
        if duration > time_left:

            # Entire time left < duration then ignore this task
            if sum(time_occupation) < duration:
                break

            # Find the lateness to get enough time for this job
            else:
                time_needed = duration - time_left
                extra_time_pointer = ddl
                while time_needed > 0:
                    lateness += 1
                    if time_occupation[extra_time_pointer] == 1:
                        time_needed -= 1
                    extra_time_pointer += 1

        do_if_late = False

        if lateness > 0:
            updated_density = this_job.get_late_benefit(lateness) / duration
            j = i + 1
            while j < len(sorted_densities):
                next_job_index = sorted_densities[j][0]
                # next_job_density = sorted_densities[j][1]

                next_job_index_in_tasks = next_job_index - 1
                next_job = tasks[next_job_index_in_tasks]

                next_job_ddl = next_job.get_deadline()
                next_job_duration = next_job.get_duration()

                next_job_lateness = 0
                next_job_time_left = sum(time_occupation[:next_job_ddl])

                possible_to_finish_next_job = True

                next_job_extra_time_pointer = next_job_ddl

                if next_job_duration > next_job_time_left:

                    # Entire time left < duration then ignore this task
                    if sum(time_occupation) < next_job_duration:
                        possible_to_finish_next_job = False

                    # Find the lateness to get enough time for this job
                    else:
                        time_needed = duration - next_job_time_left
                        extra_time_pointer = ddl
                        while time_needed > 0:
                            next_job_lateness += 1
                            if time_occupation[next_job_extra_time_pointer] == 1:
                                time_needed -= 1
                            next_job_extra_time_pointer += 1

                if possible_to_finish_next_job:
                    updated_next_job_density = next_job.get_late_benefit(next_job_lateness) / next_job.get_duration()

                    if ddl + lateness <= 1440 and (updated_density > updated_next_job_density):
                        do_if_late = True
                        break

                j += 1

        else:
            pointer = ddl - 1
            while duration > 0:
                if time_occupation[pointer] == 1:
                    time_occupation[pointer] = 0
                    duration -= 1
                    time_description[pointer] = job_index
                pointer -= 1

        if do_if_late:
            duration_copy = duration

            pointer = ddl - 1 + lateness

            while duration_copy > 0:
                try:
                    if time_occupation[pointer] == 1:
                        time_occupation[pointer] = 0
                        duration_copy -= 1
                        time_description[pointer] = job_index
                    pointer -= 1
                except IndexError:
                    print("Job index: ", job_index, "; Duration: ", duration, "; Lateness: ", lateness,
                          "; ddl: ", ddl, "; Time left: ", time_left)
                    break

    free_slots = 0
    last_free_slot = -1
    for i in range(len(time_description)):
        if time_description[i] == 0:
            free_slots += 1
            last_free_slot = i

    latest_finished_time = last_free_slot + 1
    start_time = latest_finished_time - free_slots

    job_sequence = get_sequence_pro(time_description)

    job_added = False
    first_round = True
    while free_slots > 0 and (first_round or job_added):
        first_round = False
        job_added = False

        applicable_jobs = []
        for job in tasks:
            if job.get_task_id() not in job_sequence and job.get_duration() < free_slots:
                applicable_jobs.append(job)

        potential_profit = -1
        potential_index = -1
        potential_duration = 1441
        potential_job = None

        for job in applicable_jobs:
            job_profit = job.get_late_benefit(start_time + job.get_duration() - job.get_deadline())
            if job_profit >= potential_profit and job.get_duration() < potential_duration:
                job_added = True
                potential_profit = job_profit
                potential_index = job.get_task_id()
                potential_duration = job.get_duration()
                potential_job = job

        if job_added:
            job_sequence.append(potential_index)
            start_time += potential_duration
            free_slots -= potential_duration

    return job_sequence


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


def get_sequence_pro(time_description):
    last = -1
    cluster_sequence = []
    for i in range(len(time_description)):
        curr = time_description[i]
        if curr != 0 and curr != last:
            cluster_sequence.append(curr)
        last = curr

    the_sequence = []
    for i in range(len(cluster_sequence)):
        curr_job = cluster_sequence[i]
        if curr_job not in the_sequence:
            the_sequence.append(curr_job)
        else:
            the_sequence.remove(curr_job)
            the_sequence_copy = the_sequence.copy()

            the_sequence_copy.append(curr_job)
            the_sequence.insert(len(the_sequence) - 1, curr_job)

            profit_of_the_sequence = calculate_profit(the_sequence)
            profit_of_the_copy = calculate_profit(the_sequence_copy)
            if profit_of_the_sequence >= profit_of_the_copy:
                pass
            else:
                the_sequence = the_sequence_copy

    return the_sequence


def uniqueness(jobs):
    unique_jobs = []
    for x in jobs:
        if x not in unique_jobs and x != 0:
            unique_jobs.append(x)
    return unique_jobs


def calculate_profit(id_list):
    profit = 0
    curr_t = 0
    for i in range(len(id_list)):
        curr_t += tasks[id_list[i] - 1].get_duration()
        profit += tasks[id_list[i] - 1].get_late_benefit(curr_t - tasks[id_list[i] - 1].get_deadline())
    return profit


def sanity_checker(sequence):
    total_time = 0
    seen = set()
    for job_index in sequence:
        if job_index in seen:
            print("Error")
            break
        seen.add(job_index)
        total_time += tasks[job_index - 1].get_duration()
    print(total_time)


if __name__ == '__main__':
    # better_count = 0
    # for input_path in os.listdir('small/'):
    #     tasks = read_input_file('small/' + input_path)
    #
    #     output_2_2 = solver_s.solve(tasks)
    #     output_2_2_profit = calculate_profit(output_2_2)
    #
    #     old_output = parse.read_output_file('outputs_v2/small/'+input_path[:-3] + '.out')
    #     old_output_profit = calculate_profit(old_output)
    #
    #     # og_tasks = read_input_file('medium/' + input_path)
    #     #
    #     # output_2 = solver_s.solve(og_tasks)
    #     # output_2_profit = calculate_profit(output_2)
    #
    #     output = None
    #     if output_2_2_profit >= old_output_profit:
    #         better_count += 1
    #         output = output_2_2
    #         # output_winner = "B"
    #     else:
    #         output = old_output
    #         # output_winner = "S"
    #
    #     output_path = 'outputs/small/' + input_path[:-3] + '.out'
    #     write_output_file(output_path, output)
    # print(better_count)
    #
    # better_count = 0
    # for input_path in os.listdir('medium/'):
    #     tasks = read_input_file('medium/' + input_path)
    #
    #     output_2_2 = solver_s.solve(tasks)
    #     output_2_2_profit = calculate_profit(output_2_2)
    #
    #     old_output = parse.read_output_file('outputs_v2/medium/' + input_path[:-3] + '.out')
    #     old_output_profit = calculate_profit(old_output)
    #
    #     # og_tasks = read_input_file('medium/' + input_path)
    #     #
    #     # output_2 = solver_s.solve(og_tasks)
    #     # output_2_profit = calculate_profit(output_2)
    #
    #     output = None
    #     if output_2_2_profit >= old_output_profit:
    #         better_count += 1
    #         output = output_2_2
    #         # output_winner = "B"
    #     else:
    #         output = old_output
    #         # output_winner = "S"
    #
    #     output_path = 'outputs/medium/' + input_path[:-3] + '.out'
    #     write_output_file(output_path, output)
    # print(better_count)
    #
    # better_count = 0
    # for input_path in os.listdir('large/'):
    #     tasks = read_input_file('large/' + input_path)
    #
    #     output_2_2 = solver_s.solve(tasks)
    #     output_2_2_profit = calculate_profit(output_2_2)
    #
    #     old_output = parse.read_output_file('outputs_v2/large/' + input_path[:-3] + '.out')
    #     old_output_profit = calculate_profit(old_output)
    #
    #     # og_tasks = read_input_file('medium/' + input_path)
    #     #
    #     # output_2 = solver_s.solve(og_tasks)
    #     # output_2_profit = calculate_profit(output_2)
    #
    #     output = None
    #     if output_2_2_profit >= old_output_profit:
    #         better_count += 1
    #         output = output_2_2
    #         # output_winner = "B"
    #     else:
    #         output = old_output
    #         # output_winner = "S"
    #
    #     output_path = 'outputs/large/' + input_path[:-3] + '.out'
    #     write_output_file(output_path, output)
    # print(better_count)

    for input_path in os.listdir('inputs/small/'):
        tasks = read_input_file('inputs/small/' + input_path)

        output_1 = solve(tasks)
        output_1_profit = calculate_profit(output_1)

        og_tasks = read_input_file('inputs/small/' + input_path)

        output_2 = solver_s.solve(og_tasks)
        output_2_profit = calculate_profit(output_2)

        output = None
        if output_1_profit >= output_2_profit:
            output = output_1
        else:
            output = output_2

        output_path = 'outputs/small/' + input_path[:-3] + '.out'
        write_output_file(output_path, output)

    for input_path in os.listdir('inputs/medium/'):
        tasks = read_input_file('inputs/medium/' + input_path)

        output_1 = solve(tasks)
        output_1_profit = calculate_profit(output_1)

        og_tasks = read_input_file('inputs/medium/' + input_path)

        output_2 = solver_s.solve(og_tasks)
        output_2_profit = calculate_profit(output_2)

        output = None
        if output_1_profit >= output_2_profit:
            output = output_1
        else:
            output = output_2

        output_path = 'outputs/medium/' + input_path[:-3] + '.out'
        write_output_file(output_path, output)

    for input_path in os.listdir('inputs/large/'):
        tasks = read_input_file('inputs/large/' + input_path)

        output_1 = solve(tasks)
        output_1_profit = calculate_profit(output_1)

        og_tasks = read_input_file('inputs/large/' + input_path)

        output_2 = solver_s.solve(og_tasks)
        output_2_profit = calculate_profit(output_2)

        output = None
        if output_1_profit >= output_2_profit:
            output = output_1
        else:
            output = output_2

        output_path = 'outputs/large/' + input_path[:-3] + '.out'
        write_output_file(output_path, output)
