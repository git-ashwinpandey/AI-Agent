import os, subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(target_dir):
        return f'Error: File "{file_path}" not found.'
    
    if not target_dir.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    cmd = ["python", target_dir] + args
    try:
        completed_process = subprocess.run(cmd, timeout=30, cwd=abs_working_dir, capture_output=True, text=True)
        result_string = []

        if completed_process.stdout:
            result_string.append(f"STDOUT: {completed_process.stdout}")
        
        if completed_process.stderr:
            result_string.append(f"STDERR: {completed_process.stderr}")
        
        if not completed_process.returncode == 0:
            result_string.append(f"Process exited with code {completed_process.returncode}")
        
        if not result_string:
            return "No output produced."
        
        return '\n'.join(result_string)
        
    except Exception as e:
        return f"Error listing files: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)