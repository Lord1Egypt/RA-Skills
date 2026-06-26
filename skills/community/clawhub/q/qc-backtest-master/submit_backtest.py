import os
import sys
import argparse
import time
from qc_api.client import QCApiClient
from qc_api.config import get_default_project_id

def get_project_files(main_file_path):
    """
    Reads the specified main file and other relevant data files in the same directory.
    Returns a list of dicts: [{'name': 'main.py', 'content': '...'}]
    """
    if not os.path.isfile(main_file_path):
        print(f"Error: {main_file_path} is not a valid file.")
        return []

    files_list = []
    base_dir = os.path.dirname(main_file_path)

    # 1. Add the main strategy file (renamed to main.py for QuantConnect)
    try:
        with open(main_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        files_list.append({'name': 'main.py', 'content': content})
        print(f"Added main file: {os.path.basename(main_file_path)} -> main.py")
    except Exception as e:
        print(f"Failed to read main file: {e}")
        return []

    # 2. Optionally add other relevant files in the same directory (excluding .py files to avoid conflicts)
    valid_data_extensions = {'.json', '.txt', '.csv'}
    for file in os.listdir(base_dir):
        ext = os.path.splitext(file)[1]
        if ext in valid_data_extensions:
            full_path = os.path.join(base_dir, file)
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                files_list.append({'name': file, 'content': content})
                print(f"Added data file: {file}")
            except Exception as e:
                print(f"Skipping data file {file}: {e}")

    return files_list

def main():
    parser = argparse.ArgumentParser(description="Submit a specific strategy file to QuantConnect")
    parser.add_argument("--main-file", required=True, help="Path to the main strategy .py file")
    parser.add_argument("--project-id", type=int, default=get_default_project_id(), help="QuantConnect Project ID")
    parser.add_argument("--name", help="Backtest Name", default=None)

    args = parser.parse_args()

    client = QCApiClient()
    print(f"Initializing Backtest for Project ID: {args.project_id}")

    # 1. Update Files
    print("Preparing files for sync...")
    files = get_project_files(args.main_file)
    if not files:
        print("No valid files found to sync!")
        sys.exit(1)

    # Delete old Main.py (capital M) to avoid running stale code
    print("Deleting old Main.py from cloud project...")
    try:
        client.delete_file(args.project_id, 'Main.py')
        print("Old Main.py deleted.")
    except Exception as e:
        print(f"Could not delete Main.py (may not exist): {e}")

    print("Uploading new files...")
    client.update_project_files(args.project_id, files)
    print(f"Synced {len(files)} files to QuantConnect.")

    # 2. Compile
    print("Compiling project...")
    compile_result = client.create_compile(args.project_id)
    compile_id = compile_result['compileId']

    # Wait for compilation
    while True:
        status = client.read_compile(args.project_id, compile_id)
        state = status['state']

        if state == "BuildSuccess":
            print("Compilation Successful")
            break
        elif state == "BuildError":
            print("Compilation Failed!")
            if 'logs' in status and status['logs']:
                for log in status['logs']:
                    print(f"  {log}")
            sys.exit(1)

        time.sleep(1)

    # 3. Create Backtest
    # Default name to filename without extension + timestamp
    default_name = f"{os.path.splitext(os.path.basename(args.main_file))[0]}_{int(time.time())}"
    bt_name = args.name if args.name else default_name
    print(f"Starting Backtest: {bt_name}")

    bt_result = client.create_backtest(args.project_id, compile_id, bt_name)

    bt_obj = bt_result.get('backtest', bt_result)
    if 'backtestId' in bt_obj:
        backtest_id = bt_obj['backtestId']
        print(f"Backtest Created. ID: {backtest_id}")
        # Used by run_workflow.py to capture ID
        print(f"OUTPUT_BACKTEST_ID:{backtest_id}")
    else:
        print(f"Failed to create backtest: {bt_result.get('errors', ['Unknown error'])}")
        sys.exit(1)


if __name__ == "__main__":
    main()
