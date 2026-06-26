#!/usr/bin/env python3
"""
Whoop Guru - Main Entry Point
"""
import sys
import os
import subprocess

# Add lib to path
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SKILL_DIR, 'lib'))

def main():
    if len(sys.argv) == 1:
        print("Whoop Guru - WHOOP Health Management System")
        print("Usage: whoop-guru [command]")
        print("Commands:")
        print("  status   - Show current status")
        print("  score    - Show health score")
        print("  report   - Generate report")
    else:
        cmd = sys.argv[1]
        
        if cmd == "status":
            # Get data from skill's data directory
            data_file = os.path.join(SKILL_DIR, 'data', 'processed', 'latest.json')
            
            try:
                import json
                with open(data_file) as f:
                    data = json.load(f)
                processed = data.get('processed', {})
                recovery = processed.get('recovery', [])
                if recovery:
                    r = recovery[0]
                    print(f"\n📊 今日状态 ({r.get('date', 'N/A')})")
                    print(f"   恢复: {r.get('recovery_score')}%")
                    print(f"   HRV: {r.get('hrv')} ms")
                    print(f"   RHR: {r.get('rhr')} bpm")
            except Exception as e:
                print(f"数据获取失败: {e}")
                
        elif cmd == "score":
            script_path = os.path.join(SKILL_DIR, 'lib', 'health_score.py')
            subprocess.run(['python3', script_path], check=False)
        elif cmd == "report":
            script_path = os.path.join(SKILL_DIR, 'lib', 'enhanced_report.py')
            subprocess.run(['python3', script_path], check=False)
        else:
            print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
