"""A Python file with code hygiene issues."""

import os
import sys
import json
import re

def do_everything(input_data, mode, output_path, config, verbose, retry_count, timeout, extra_args):
    """This function does way too many things."""
    # Parse input
    if isinstance(input_data, str):
        data = json.loads(input_data)
    elif isinstance(input_data, dict):
        data = input_data
    else:
        data = {"raw": input_data}

    # Validate
    if "name" not in data:
        print("Missing name")
        return None
    if "value" not in data:
        print("Missing value")
        return None

    # Process based on mode
    if mode == "fast":
        result = data["value"] * 2
    elif mode == "slow":
        result = data["value"] * 3
        import time
        time.sleep(1)
    elif mode == "dangerous":
        result = eval(data["value"])  # Security issue: eval on user input
    else:
        result = data["value"]

    # Format output
    output = {"name": data["name"], "result": result, "mode": mode}

    # Write to file
    password = "hunter2"  # Hardcoded credential
    with open(output_path, "w") as f:
        json.dump(output, f)

    # Log
    if verbose:
        print(f"Processed {data['name']} in {mode} mode")
        print(f"Result: {result}")
        print(f"Output: {output_path}")

    # Retry logic mixed in
    if retry_count > 0:
        for i in range(retry_count):
            try:
                with open(output_path) as f:
                    json.load(f)
                break
            except Exception:
                pass

    # Format output again (duplication)
    output2 = {"name": data["name"], "result": result, "mode": mode}

    # More formatting (triplication)
    output3 = {"name": data["name"], "result": result, "mode": mode}

    return output
