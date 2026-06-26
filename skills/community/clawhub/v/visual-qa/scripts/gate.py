#!/usr/bin/env python3
"""
All-in-one visual QA gate: capture + diff in a single command.
"""

import argparse
import json
import os
import sys
import tempfile
import subprocess
from pathlib import Path

def run_capture(args, config, current_dir):
    """Run capture.py to generate current screenshots."""
    capture_script = os.path.join(os.path.dirname(__file__), 'capture.py')
    
    cmd = [sys.executable, capture_script]
    
    # Build URL(s) from config or args
    if config.get('urls'):
        # Write a temp config that uses current_dir instead of baselineDir
        temp_config = config.copy()
        temp_config.pop('baselineDir', None)  # Remove baselineDir from config
        
        temp_config_path = os.path.join(current_dir, '.temp-config.json')
        with open(temp_config_path, 'w') as f:
            json.dump(temp_config, f)
        
        cmd.extend(['--config', temp_config_path])
    elif args.url:
        cmd.append(args.url)
    elif config.get('baseUrl'):
        cmd.append(config['baseUrl'])
    else:
        print("❌ No URL or config provided")
        return False
    
    cmd.extend(['--output', current_dir])
    
    # Viewports from args or config
    viewports = args.viewports or config.get('viewports')
    if viewports:
        cmd.extend(['--viewports'] + viewports)
    
    # Server from args or config
    server = args.server or config.get('server')
    if server:
        cmd.extend(['--server', server])
    
    # Port from args or config
    port = args.port or config.get('port')
    if port:
        cmd.extend(['--port', str(port)])
    
    print(f"🔧 Running capture...")
    result = subprocess.run(cmd)
    
    return result.returncode == 0

def run_diff(baseline_dir, current_dir, diff_dir, threshold):
    """Run diff.py to compare screenshots."""
    diff_script = os.path.join(os.path.dirname(__file__), 'diff.py')
    
    cmd = [
        sys.executable, diff_script,
        '--baseline', baseline_dir,
        '--current', current_dir,
        '--output', diff_dir,
        '--threshold', str(threshold)
    ]
    
    print(f"\n🔍 Running diff...")
    result = subprocess.run(cmd)
    
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser(
        description='All-in-one visual QA gate: capture + diff',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic gate with URL
  %(prog)s --baseline .visual-qa/baselines --url http://localhost:3000

  # With local dev server
  %(prog)s --baseline .visual-qa/baselines --server "npm run dev" --port 3000

  # Using config file
  %(prog)s --config .visual-qa.json

  # Custom threshold
  %(prog)s --baseline .visual-qa/baselines --url http://localhost:3000 --threshold 95

Exit codes:
  0 = Visual QA passed (all screenshots within threshold)
  1 = Visual QA failed (one or more screenshots differ)

Config file format (.visual-qa.json):
  {
    "urls": ["/", "/about", "/pricing"],
    "baseUrl": "http://localhost:3000",
    "viewports": ["desktop", "mobile"],
    "threshold": 99,
    "server": "npm run dev",
    "port": 3000,
    "baselineDir": ".visual-qa/baselines"
  }
        """
    )
    
    parser.add_argument('--config', help='Path to config JSON file')
    parser.add_argument('--baseline', '-b', help='Baseline screenshots directory (required if no config)')
    parser.add_argument('--url', help='URL to capture (or use --config)')
    parser.add_argument('--viewports', '-v', nargs='+', 
                       choices=['desktop', 'tablet', 'mobile'],
                       help='Viewport sizes to capture')
    parser.add_argument('--server', help='Command to start local dev server')
    parser.add_argument('--port', type=int, help='Server port')
    parser.add_argument('--threshold', '-t', type=float, default=99.0,
                       help='Similarity threshold percentage (default: 99.0)')
    parser.add_argument('--keep-current', action='store_true',
                       help='Keep current screenshots after comparison (default: delete)')
    parser.add_argument('--keep-diffs', action='store_true',
                       help='Keep diff images after comparison (default: delete on pass)')
    
    args = parser.parse_args()
    
    # Load config if provided
    config = {}
    if args.config:
        try:
            with open(args.config) as f:
                config = json.load(f)
        except Exception as e:
            print(f"❌ Failed to load config: {e}")
            sys.exit(1)
    
    # Determine baseline directory
    baseline_dir = args.baseline or config.get('baselineDir')
    if not baseline_dir:
        print("❌ No baseline directory provided. Use --baseline or config file")
        parser.print_help()
        sys.exit(1)
    
    if not os.path.isdir(baseline_dir):
        print(f"❌ Baseline directory not found: {baseline_dir}")
        print(f"\nCreate baselines first:")
        print(f"  python3 {os.path.join(os.path.dirname(__file__), 'capture.py')} --output {baseline_dir} ...")
        sys.exit(1)
    
    # Determine threshold
    threshold = config.get('threshold', args.threshold)
    
    # Create temporary directories for current screenshots and diffs
    with tempfile.TemporaryDirectory() as temp_dir:
        current_dir = os.path.join(temp_dir, 'current')
        diff_dir = os.path.join(temp_dir, 'diffs')
        os.makedirs(current_dir)
        os.makedirs(diff_dir)
        
        print("="*60)
        print("VISUAL QA GATE")
        print("="*60)
        print(f"Baseline: {baseline_dir}")
        print(f"Threshold: {threshold}%")
        print("="*60)
        print()
        
        # Step 1: Capture current screenshots
        if not run_capture(args, config, current_dir):
            print("\n❌ Capture failed")
            sys.exit(1)
        
        # Step 2: Compare against baselines
        passed = run_diff(baseline_dir, current_dir, diff_dir, threshold)
        
        # Optionally copy current screenshots and diffs to persistent location
        if args.keep_current:
            keep_current_dir = '.visual-qa/current'
            os.makedirs(keep_current_dir, exist_ok=True)
            subprocess.run(['cp', '-r', f'{current_dir}/.', keep_current_dir])
            print(f"\n📁 Current screenshots saved to: {keep_current_dir}")
        
        if args.keep_diffs or not passed:
            keep_diff_dir = '.visual-qa/diffs'
            os.makedirs(keep_diff_dir, exist_ok=True)
            subprocess.run(['cp', '-r', f'{diff_dir}/.', keep_diff_dir])
            print(f"📁 Diff images saved to: {keep_diff_dir}")
        
        # Exit with appropriate code
        if passed:
            print("\n" + "="*60)
            print("✓ VISUAL QA GATE PASSED")
            print("="*60)
            sys.exit(0)
        else:
            print("\n" + "="*60)
            print("✗ VISUAL QA GATE FAILED")
            print("="*60)
            print(f"\nReview diff images to see what changed.")
            if not args.keep_diffs:
                print(f"Diff images were saved to: .visual-qa/diffs")
            print(f"\nIf changes are intentional, update baselines:")
            print(f"  rm -rf {baseline_dir}")
            print(f"  python3 {os.path.join(os.path.dirname(__file__), 'capture.py')} --output {baseline_dir} ...")
            sys.exit(1)

if __name__ == '__main__':
    main()
