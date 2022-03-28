import parse
import Task

# parameters
filepath = "150"
dummy_intervals = [0, 6, 13, 21, 40]
num_copies = len(dummy_intervals)

# read in tasks
og_tasks = parse.read_input_file(filepath + '.in')
og_n = len(og_tasks)
tasks = og_tasks

# since 1 task has several "id"s, find the id of the task that spawned the others
def find_original_id (id):
    while (id > (og_n+1)):
        id = int(id / 10)
    return id

# make the dummy tasks. The ids of each dummy of task with id x is x*10, x*100, etc
expanded_tasks = []
for i in range(len(tasks)):
    for j in range(0, num_copies):
        curr_task = tasks[i]
        curr_id = curr_task.get_task_id()*(10**j)
        curr_deadline = curr_task.get_deadline() + dummy_intervals[j]
        curr_duration = curr_task.get_duration()

        if curr_deadline > 1440:
            curr_profit = 0
        else:
            #s = curr_duration - curr_deadline
            s = dummy_intervals[j]
            curr_profit = curr_task.get_late_benefit(s)

        dummy_task = Task.Task(curr_id, curr_deadline, curr_duration, curr_profit)
        expanded_tasks.append(dummy_task)

# sort all the tasks by increasing deadline
tasks = expanded_tasks
sorted_tasks = []
while len(tasks) > 0:
    min_task = tasks[0]
    for i in range(len(tasks)):
        if tasks[i].get_deadline() < min_task.get_deadline():
            min_task = tasks[i]
    sorted_tasks.append(min_task)
    tasks.remove(min_task)

# d is task with longest deadline, n is number of expanded tasks
d = 1440
# sorted_tasks[len(sorted_tasks)-1].get_deadline()
n = len(sorted_tasks)

# init used matrix
used = []
for i in range(n+1):
    used.append([])
for t in range(d+1):
    for i in range(n+1):
        used[i].append([])

# truncate at 1440
def truncate(seq):
    curr_t = 0
    i = 0
    while i < len(seq):
        curr_t += og_tasks[seq[i] - 1].get_duration()
        if curr_t >= 1440:
            break
        i += 1
    truncated_seq = seq[:i]
    truncated_seq_len = calculate_total_time(truncated_seq)

    # find anything to insert at the end
    # best_insert_task = -1
    # best_benefit = -1
    # for j in range(len(og_tasks)):
    #     if not (og_tasks[j].get_task_id() in truncated_seq):
    #         finish_time = og_tasks[j].get_duration() + truncated_seq_len
    #         if finish_time < 1440:
    #             late_time = finish_time - og_tasks[j].get_deadline()
    #             benefit = og_tasks[j].get_late_benefit(late_time)
    #             if benefit > best_benefit:
    #                 best_benefit = benefit
    #                 best_insert_task = og_tasks[j].get_task_id()
    #
    # betterseq = truncated_seq.copy()
    # if best_benefit > 0:
    #     betterseq.append(best_insert_task)
    # return betterseq

    time_so_far = calculate_total_time(truncated_seq)
    free_slots = 1440 - time_so_far
    start_time = time_so_far + 1

    job_added = False
    first_round = True
    while free_slots > 0 and (first_round or job_added):
        first_round = False
        job_added = False

        applicable_jobs = []
        for job in tasks:
            if job.get_task_id() not in truncated_seq and job.get_duration() < free_slots:
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
            truncated_seq.append(potential_index)
            start_time += potential_duration
            free_slots -= potential_duration

    return truncated_seq

# calculate profit from a sequence
def calculate_profit(id_list):
    profit = 0
    curr_t = 0
    for i in range(len(id_list)):
        curr_t += og_tasks[id_list[i]-1].get_duration()
        if curr_t > 1440:
            break
        profit += og_tasks[id_list[i]-1].get_late_benefit(curr_t - og_tasks[id_list[i]-1].get_deadline())
    return profit

# calculate total time taken by sequence
def calculate_total_time(id_list):
    curr_t = 0
    for i in range(len(id_list)):
        curr_t += og_tasks[id_list[i]-1].get_duration()
    return curr_t

# init the B matrix
B = []
for i in range(n+1):
    B.append([])

for t in range(d+1):
    for i in range(n+1):
        B[i].append(0)

# ... do the dynamic programming
for i in range(1, n+1):
    for t in range(d+1):
        t_prime = min(t, sorted_tasks[i-1].get_deadline()) - sorted_tasks[i-1].get_duration()
        og_id = find_original_id(sorted_tasks[i - 1].get_task_id())

        if t_prime < 0:
            used[i][t] = used[i - 1][t].copy()
            B[i][t] = B[i - 1][t]
        else:
            # B[i][t] = max(B[i-1][t], sorted_tasks[i-1].get_max_benefit() + B[i-1][t_prime])
            RHS_seq = used[i - 1][t_prime].copy()
            if og_id in used[i - 1][t_prime]:
                RHS_seq.remove(og_id)
            RHS_seq.append(og_id)
            profit_RHS = calculate_profit(RHS_seq)

            if B[i - 1][t] > profit_RHS:
                used[i][t] = used[i - 1][t].copy()
                B[i][t] = B[i-1][t]
            else:
                B[i][t] = profit_RHS
                used[i][t] = RHS_seq

# check if any element in a list is repeated
def check_unique(id_list):
    uniques = []
    bad = 0
    for id in id_list:
        if id in uniques:
            print("BAD BAD BAD, id", id, "was repeated")
            bad = 1
        else:
            uniques.append(id)
    if bad == 0:
        print("the sequence is nice and unique")

# OUTPUT
sequence = truncate(used[n][d])
print("filepath: ", filepath)
print("number of copies: ", num_copies)
print("the sequence is: ")
print(sequence)
check_unique(sequence)
profit_used = calculate_profit(sequence)
print("checked profit in seq is", profit_used)
print("total time is ", calculate_total_time(sequence))

#parse.write_output_file(filepath + ".out", used[n][d])