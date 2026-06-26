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
        # Whitelist specific environment variables to minimize blast radius
        # and comply with ClawHub security health requirements.
        safe_env = {
            k: v for k, v in os.environ.items() 
            if k.startswith("TRUNKATE_") or k.startswith("OPENCLAW_") or k == "PATH"
        }
        
        subprocess.run(
            [sys.executable, script_path], 
            env=safe_env, 
            check=True
        )
    except subprocess.CalledProcessError as e:
        # The activator failed; pre_request continues without optimization
        pass

if __name__ == "__main__":
    main()