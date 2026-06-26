#!/usr/bin/env python3
"""
Whoop Guru CLI - Self-contained version
"""
import sys
import os
import subprocess

# Get skill directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(SKILL_DIR, 'data')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')

def get_status():
    """Show current status from local data"""
    latest_file = os.path.join(PROCESSED_DIR, 'latest.json')
    
    if not os.path.exists(latest_file):
        print("No data found. Run 'fetch' first.")
        return
    
    try:
        import json
        with open(latest_file) as f:
            data = json.load(f)
        
        processed = data.get('processed', {})
        recovery = processed.get('recovery', [])
        sleep = processed.get('sleep', [])
        cycles = processed.get('cycles', [])
        
        if recovery:
            r = recovery[0]
            print(f"\n📊 今日状态 ({r.get('date', 'N/A')})")
            print(f"   恢复: {r.get('recovery_score')}%")
            print(f"   HRV: {r.get('hrv')} ms")
            print(f"   RHR: {r.get('rhr')} bpm")
        
        if recovery and sleep:
            print(f"\n🔋 身体电量")
            rec = recovery[0].get('recovery_score', 50)
            sp = sleep[0].get('sleep_performance', 70) if sleep else 70
            battery = rec * 0.6 + sp * 0.4
            level = "🟢" if battery >= 80 else "🟡" if battery >= 60 else "🟠" if battery >= 40 else "🔴"
            print(f"   电量: {battery:.0f}% {level}")
            
    except Exception as e:
        print(f"Error: {e}")

def fetch_data():
    """Fetch WHOOP data"""
    fetcher = os.path.join(SCRIPT_DIR, 'whoop-fetcher.sh')
    subprocess.run([fetcher, 'all', '7'])
    
    # Process
    subprocess.run(['python3', __file__, 'process'])

def process_data():
    """Process raw data"""
    processor = os.path.join(SCRIPT_DIR, 'data_processor.py')
    subprocess.run(['python3', processor])

def main():
    if len(sys.argv) == 1:
        print("Whoop Guru - WHOOP Health Management System")
        print("Usage: cli.py [command]")
        print("Commands:")
        print("  status   - Show current status")
        print("  fetch    - Fetch WHOOP data")
        print("  process  - Process data")
        print("  report   - Generate report")
    else:
        cmd = sys.argv[1]
        
        if cmd == 'status':
            get_status()
        elif cmd == 'fetch':
            fetch_data()
        elif cmd == 'process':
            process_data()
        elif cmd == 'report':
            get_status()
            # Import and run report generator
            try:
                import json
                with open(os.path.join(PROCESSED_DIR, 'latest.json')) as f:
                    data = json.load(f)
                print("\n✅ Data loaded for report generation")
            except:
                print("No data. Run 'fetch' first.")
        else:
            print(f"Unknown command: {cmd}")

if __name__ == '__main__':
    main()
