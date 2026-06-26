#!/usr/bin/env python3
import subprocess
import os
import sys

def main():
    """
    Triggers the Trunkate activator logic during the PreRequest lifecycle.
    Ensures environment variables are passed to the sub-process for 
    threshold evaluation.
    """
    script_path = os.path.join("scripts", "activator.py")
    
    if not os.path.exists(script_path):
        print(f"Trunkate Alert: {script_path} not found.", file=sys.stderr)
        return

    try:
        # Pass current environment (containing OpenClaw state) to the sub-process
        subprocess.run(
            [sys.executable, script_path], 
            env=os.environ.copy(), 
            check=True
        )
    except subprocess.CalledProcessError as e:
        # The activator failed; pre_request continues without optimization
        pass

if __name__ == "__main__":
    main()