import subprocess
import time
import psutil
import os
import re

"""
status: 
    0: Accepted
    1: Wrong Answer
    2: Time Limit Exceeded
    3: Compilation Error
"""

def pars_output(output:str) -> str:
    """
    Decode the output from bytes to string
    """
    res = " ".join(re.split(r'[\t\r\n ]+', output))
    return res  


def compile_lang(lang:str, code:str) -> list[str]:
    """
    Compile the code and return the command to run it
    """
    if lang == "py":
        with open("tmp/temp.py", "w") as f:
            f.write(code)
        return ["python", "./tmp/temp.py"]
    elif lang == "c":
        with open("tmp/temp.c", "w") as f:
            f.write(code)

        # Compile the code
        compile_process = subprocess.run(['gcc', 'tmp/temp.c', '-o', 'tmp/temp.exe'], capture_output=True, text=True)
        if compile_process.returncode != 0:
            return None
        return ["./tmp/temp.exe"]
    else :
        return None

def run_code(code:str, input_data:str, output_data:str, lang:str, time_limit:int=2):
    """
    Execute the code and compare the output with the expected output
    """
    result = {
        "status": -1,
        "execution_time": 0,
        "difference": []
    }

    cmd = compile_lang(lang, code)
    if cmd is None:
        result['status'] = 3
        return result

    # Measure execution time and memory usage
    start_time = time.time()
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.stdin.write(input_data.encode())
    # Wait for the process to complete and capture output
    try:
        stdout, stderr = process.communicate(timeout=time_limit)
        end_time = time.time()
    except subprocess.TimeoutExpired:
        result['status'] = 2
        result['execution_time'] = time_limit
        process.kill()
        return result

    result['execution_time'] = end_time - start_time
    
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

    result["difference"] = difference
    result["status"] = 0 if len(difference) == 0 else 1
    return result
