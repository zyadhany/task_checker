import os
from checker import run_code

"""
   get code from subbmtions folder
   run it with test cases input and output files
    return result of each student
"""

status = {
    0: "Accepted",
    1: "Wrong Answer",
    2: "Time Limit Exceeded",
    3: "Compilation Error"
}

# Ensure the task and test folders exist
task_folder = os.path.join(os.path.dirname(__file__), "files")
test_folder = os.path.join(os.path.dirname(__file__), "tests")

if not os.path.exists(task_folder):
    raise FileNotFoundError(f"The task folder {task_folder} does not exist.")
if not os.path.exists(test_folder):
    raise FileNotFoundError(f"The test folder {test_folder} does not exist.")

def read_file(file):
    """
    Read the content of the file
    """
    with open(file, "r") as f:
        return f.read()

def get_files(folder):
    """
    Get all files from the specified folder
    """
    return os.listdir(folder)

def main():
    # get all files from task and test folder
    files = get_files(task_folder)
    tests = get_files(test_folder)
    
    # result of each student
    result = {}

    for file in files:
        # get the name of the student
        student = file.split(".")[0]

        # get the language of the code
        lang = file.split(".")[-1]

        # initialize the result of the student
        result[student] = None
        
        # get the code
        code = read_file(os.path.join(task_folder, file))
        
        # get the test cases
        for test in tests:
            # get the name of the test case
            test_name = test.split(".")[0]

            # check if the test case is an input file
            if test.split(".")[1] != "in":
                continue

            # get the input
            input_data = read_file(os.path.join(test_folder, test))

            # get the output
            output_data = read_file(os.path.join(test_folder, f"{test_name}.out"))
    
            # execute the code and get the result            
            statu = run_code(code, input_data, output_data, lang, 2)
            # update the result of the student
            result[student] = statu['status']
            if result[student] != 0:
                break

    # print the result of each student
    with open("result.txt", "w") as f:
        for student, statu_code in result.items():
            f.write(f"{student}: {status[statu_code]}\n")
            print(f"{student}: {status[statu_code]}")
    
if __name__ == "__main__":
    main()
