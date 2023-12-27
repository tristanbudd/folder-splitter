import os
import json
import shutil


def main():
    # Validate and fetch data from settings.json
    print("Folder Splitter | Loading settings.json")

    if not os.path.exists("settings.json"):
        print("Error | Unable to find settings.json")
        input()
        exit()

    with open("settings.json", "r") as f:
        json_data = json.load(f)

    error_count = 0
    if not json_data["debug_mode"] == True and not json_data["debug_mode"] == False:
        print("Error | Unable to load debug status from settings.json")
        error_count += 1

    if json_data["source_dir"] == "" or not os.path.exists(json_data["source_dir"]):
        print("Error | Unable to find source directory, or option is empty.")
        error_count += 1

    if not json_data["output_dir"] or json_data["output_dir"] == "":
        print("Error | Unable to output directory is empty.")
        error_count += 1

    if not str(json_data["subfolder_amount"]).isnumeric() or json_data["subfolder_amount"] < 2:
        print("Error | Sub-folder amount must be a number and greater than 1.")
        error_count += 1

    if not json_data["subfolder_name"] or not len(json_data["subfolder_name"]) > 0 or len(json_data["subfolder_name"]) > 20:
        print("Error | Sub-folder name not found, Or is above 20 characters.")
        error_count += 1

    if error_count == 0:
        print("Folder Splitter | Settings.json validated and ready to go.")

        if json_data["subfolder_amount"] > 100:
            print("Folder Splitter | Sub-folder count is above 100, this may cause issues and take extended amounts of "
                  "time. Are you sure you would like to continue? (Y/N)")

            continue_choice = input("Enter (Y/N): ")
            if continue_choice.upper() == "Y":
                print("Folder Splitter | Skipping sub-folder count check.")
            elif continue_choice.upper() == "N":
                exit()
            else:
                print("Error | Invalid Argument.")

        debug_mode = json_data["debug_mode"]
        source_folder = json_data["source_dir"]
        output_folder = json_data["output_dir"]
        num_subfolders = json_data["subfolder_amount"]
        subfolders_name = json_data["subfolder_name"]

        # Create a list of all files in the source folder and its sub-folders
        files = []
        for root, _, filenames in os.walk(source_folder):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                files.append(file_path)

        print("Folder Splitter | Beginning folder splitting process.")

        # Sort the files by size in ascending order
        files.sort(key=lambda f: os.path.getsize(f))

        # Calculate the target number of files per sub-folder
        files_per_subfolder = len(files) // num_subfolders
        remainder = len(files) % num_subfolders

        print(f"Folder Splitter | Amount Of Files: {len(files)} | Amount Per Sub-Folder: {files_per_subfolder}")

        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
            print(f"Folder Splitter | Created output folder: {output_folder}")

        # Create the sub-folders
        subfolders = [os.path.join(output_folder, f"{subfolders_name}_{i + 1}") for i in range(num_subfolders)]
        for subfolder in subfolders:
            os.makedirs(subfolder, exist_ok=True)
            if debug_mode:
                print(f"Debug | Sub-folder {subfolder} created.")

        # Distribute the files evenly among the sub-folders
        for i, file in enumerate(files):
            subfolder_index = i % num_subfolders
            destination_file = os.path.join(subfolders[subfolder_index], os.path.relpath(file, source_folder))
            os.makedirs(os.path.dirname(destination_file), exist_ok=True)
            shutil.copyfile(file, destination_file)
            if debug_mode:
                print(f"Debug | File {file} copied to {destination_file}.")

        # Distribute remaining files one by one to each sub-folder
        remaining_files = files[files_per_subfolder * num_subfolders:]
        for i, file in enumerate(remaining_files):
            subfolder_index = i % num_subfolders
            destination_file = os.path.join(subfolders[subfolder_index], os.path.relpath(file, source_folder))
            os.makedirs(os.path.dirname(destination_file), exist_ok=True)
            shutil.copyfile(file, destination_file)
            if debug_mode:
                print(f"Debug | File {file} copied to {destination_file}.")

        print("Folder Splitter | Splitting Process Complete")
        input()
    else:
        print("Folder Splitter | Please address all errors before restarting the script.")
        input()


if __name__ == "__main__":
    main()
