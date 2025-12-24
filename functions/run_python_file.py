import os
import sys
import subprocess


def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    common_path = os.path.commonpath([working_dir_abs, target_path])
    try:
        if common_path != working_dir_abs:
            print(
                f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            )
            return
        full_path = os.path.normpath(os.path.join(working_directory, file_path))
        if os.path.isfile(full_path) is False:
            print(f'Error: "{file_path}" does not exist or is not a regular file')
            return
        if full_path.endswith(".py") is False:
            print(f'Error: "{file_path}" is not a Python file')
            return
        command = ["python", target_path]
        if args is not None:
            command.extend(args)
        result: subprocess.CompletedProcess = subprocess.run(
            command,
            timeout=30,
            text=True,
            stdout=True,
            stderr=True,
            cwd=working_dir_abs,
        )
        output_string = ""
        print(result.args)
        if result.returncode != 0:
            output_string = f"Process exited with code {result.returncode}"
        if result.stdout is None and result.stderr is None:
            output_string = "No output produced\n"
        output_string += f"STDOUT: {result.stdout}\n"
        output_string += f"STDERR: {result.stderr}\n"
        print(output_string)
        return
    except Exception as e:
        print(f"Error: executing Python file: {e}")
