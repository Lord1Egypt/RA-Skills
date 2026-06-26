#!/usr/bin/env python3
"""Surge download manager wrapper"""

import argparse
import subprocess
import os
import sys

def run_surge(args_list):
    """Run surge command"""
    result = subprocess.run(['surge'] + args_list, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def start_server(output_dir=None):
    """Start surge server"""
    cmd = ['surge', 'server']
    if output_dir:
        cmd.extend(['-o', output_dir])
    
    print(f"⚡ Starting Surge server...")
    proc = subprocess.Popen(cmd)
    return proc

def main():
    parser = argparse.ArgumentParser(description='Surge download manager wrapper')
    parser.add_argument('url', help='URL to download')
    parser.add_argument('-o', '--output', default='./downloads', help='Output directory')
    parser.add_argument('--server', action='store_true', help='Start server first')
    parser.add_argument('--batch', help='Batch file with URLs')
    parser.add_argument('--list', action='store_true', help='List downloads')
    parser.add_argument('--status', action='store_true', help='Check server status')
    
    args = parser.parse_args()
    
    if args.list:
        code, stdout, stderr = run_surge(['ls'])
        print(stdout or stderr)
        return code
    
    if args.status:
        code, stdout, stderr = run_surge(['server', 'status'])
        print(stdout or stderr)
        return code
    
    # Start server if requested
    if args.server:
        start_server(args.output)
        import time
        time.sleep(2)
    
    # Build add command
    cmd = ['add', args.url, '-o', args.output]
    
    if args.batch:
        cmd = ['add', '-b', args.batch, '-o', args.output]
    
    print(f"📥 Adding: {args.url}")
    print(f"   To: {args.output}")
    
    code, stdout, stderr = run_surge(cmd)
    
    if code != 0:
        print(f"❌ Error: {stderr}")
        sys.exit(1)
    
    print(f"✅ Added to queue")
    
    # Show queue
    code, stdout, stderr = run_surge(['ls'])
    print(stdout)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
