import os
import subprocess
import time
import psutil

"""
   get code from subbmtions folder
   run it with test cases input and output files
    return result of each student
"""

# Ensure the task and test folders exist
task_folder = os.path.join(os.path.dirname(__file__), "task_1")
test_folder = os.path.join(os.path.dirname(__file__), "tests")
time_limit = 2

if not os.path.exists(task_folder):
    raise FileNotFoundError(f"The task folder {task_folder} does not exist.")
if not os.path.exists(test_folder):
    raise FileNotFoundError(f"The test folder {test_folder} does not exist.")


def pars_output(output):
    """
    Decode the output from bytes to string
    """
    res = ""
    for c in output:
        if c == ' ' or c == '\n' or c == '\t' or c == '\r':
            continue
        res += c
    return res

def exe_code(code, input_data, output_data, lang):
    """
    Execute the code and compare the output with the expected output
    """

    if lang == "py":
        with open("temp.py", "w") as f:
            f.write(code)
        cmd = f"python ./temp.py"
    elif lang == "c":
        with open("temp.c", "w") as f:
            f.write(code)

        # Compile the code
        compile_process = subprocess.run(['gcc', 'temp.c', '-o', 'temp.exe'], capture_output=True, text=True)
        if compile_process.returncode != 0:
            print("Compilation failed:")
            print(compile_process.stderr)
            exit(1)

        cmd = f"./temp.exe"
    else :
        return 0

    
    # Measure execution time and memory usage
    start_time = time.time()
    process = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pid = process.pid
    ps_process = psutil.Process(pid)

    # Wait for the process to complete and capture output
    try:
        stdout, stderr = process.communicate(timeout=time_limit)
        end_time = time.time()
    except subprocess.TimeoutExpired:
        process.kill()
        return 0

    # get execution time
    execution_time = end_time - start_time

    
    ot1 = pars_output(stdout.decode())
    ot2 = pars_output(output_data)

    # Compare the output with the expected output
    difference = []
    for i in range(min(len(ot1), len(ot2))):
        if ot1[i] != ot2[i]:
            difference.append((i, ot1[i], ot2[i]))

    if len(ot1) != len(ot2):
        longer, shorter = (ot1, ot2) if len(ot1) > len(ot2) else (ot2, ot1)
        for i in range(len(shorter), len(longer)):
            difference.append((i, longer[i], None if longer is ot1 else longer[i]))

    if ot1 == ot2:
        return 1
    else:
        return 0


def main():
    # get all files from task folder
    files = os.listdir(task_folder)
    # get all test files
    tests = os.listdir(test_folder)
    
    # result of each student
    res = {}

    for file in files:
        # get the name of the student
        student = file.split(".")[0]

        # get the language of the code
        lang = file.split(".")[1]

        # initialize the result of the student
        res[student] = 0
        
        # get the code
        with open(os.path.join(task_folder, file), "r") as f:
            code = f.read()
        
        # get the test cases
        for test in tests:
            # get the name of the test case
            test_name = test.split(".")[0]

            # check if the test case is an input file
            if test.split(".")[1] != "in":
                continue

            # get the input
            with open(os.path.join(test_folder, test), "r") as f:
                input_data = f.read()

            # get the output
            with open(os.path.join(test_folder, test_name + ".out"), "r") as f:
                output_data = f.read()

            # execute the code and get the result            
            istrue = exe_code(code, input_data, output_data, lang)

            # update the result of the student
            res[student] += istrue

    # print the result of each student
    with open("result.txt", "w") as f:
        for student, score in res.items():
            f.write(f"{student}: {score}\n")
            print(f"{student}: {score}")
    
if __name__ == "__main__":
    main()
