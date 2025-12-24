import os


def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
    common_path = os.path.commonpath([working_dir_abs, target_dir])
    try:
        if common_path != working_dir_abs:
            print(
                f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            )
            return
        full_path = os.path.normpath(os.path.join(working_directory, file_path))
        if os.path.isdir(full_path) is True:
            print(f'Error: Cannot write to "{file_path}" as it is a directory')
            return
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
            print(
                f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            )
            return
    except Exception as e:
        print(f"  Error: {e}")
