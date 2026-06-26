#!/usr/bin/env python3
"""
Portable entry point for flyai-travelmapify skill.

This script can be run from any directory and will automatically:
1. Locate the skill directory
2. Set up the Python path correctly
3. Execute the main functionality

Usage:
    python3 flyai-travelmapify.py --image /path/to/image.jpg --output-html my-travel-map.html
    python3 flyai-travelmapify.py --locations "上海外滩,迪士尼乐园,豫园" --output-html my-travel-map.html
"""

import os
import sys
import subprocess

def get_skill_dir():
    """Get the directory containing this script (the skill root)"""
    return os.path.dirname(os.path.realpath(__file__))

def main():
    # Get the skill directory
    skill_dir = get_skill_dir()
    scripts_dir = os.path.join(skill_dir, 'scripts')
    
    # Add scripts directory to Python path
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    
    # Construct the command to run the main script
    main_script = os.path.join(scripts_dir, 'main_travel_mapify_enhanced.py')
    
    if not os.path.exists(main_script):
        print(f"Error: Main script not found at {main_script}", file=sys.stderr)
        sys.exit(1)
    
    # Build the command with all arguments
    cmd = [sys.executable, main_script] + sys.argv[1:]
    
    try:
        # Execute the main script
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error running main script: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()