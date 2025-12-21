import os

MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
    common_path = os.path.commonpath([working_dir_abs, target_dir])
    try:
        if common_path != working_dir_abs:
            print(
                f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            )
            return
        full_path = os.path.join(working_directory, file_path)
        if os.path.isfile(full_path) is False:
            print(f'Error: File not found or is not a regular file: "{file_path}"')
            return
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            print(file_content_string)
            return file_content_string
    except Exception as e:
        print(f"  Error: {e}")
