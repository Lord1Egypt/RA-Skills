#!/usr/bin/env python3
"""
Manual Work Prompt System
Time-based reminders for Jira work logging (8 AM - 7 PM)
No activity monitoring, minimal resource usage
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
import subprocess
import threading
from pathlib import Path

class WorkPromptSystem:
    def __init__(self, config_file="jira_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.workspace_dir = Path(__file__).parent
        self.running = False
        
        # Work hours configuration (8 AM - 7 PM Tehran time)
        self.work_start_hour = 8
        self.work_end_hour = 19  # 7 PM
        
        # Prompt intervals (in minutes)
        self.morning_prompt = "12:00"    # Mid-day check
        self.afternoon_prompt = "16:00"  # Late afternoon check
        self.eod_prompt = "18:30"        # End of day summary
        
    def load_config(self):
        """Load configuration from JSON file"""
        if not os.path.exists(self.config_file):
            print(f"⚠️  Config file {self.config_file} not found")
            print(f"   Using default settings")
            return {}
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Error reading config: {e}")
            return {}
    
    def is_work_hours(self):
        """Check if current time is within work hours (8 AM - 7 PM)"""
        now = datetime.now()
        current_hour = now.hour
        
        # Check if within work hours
        if self.work_start_hour <= current_hour < self.work_end_hour:
            return True
        
        # Also check if it's a weekday
        if now.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            return False
        
        return False
    
    def send_notification(self, title, message):
        """Send macOS notification"""
        try:
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(['osascript', '-e', script], capture_output=True)
            print(f"📢 Notification sent: {title}")
            return True
        except Exception as e:
            print(f"❌ Failed to send notification: {e}")
            return False
    
    def run_jira_log(self):
        """Run the Jira log script"""
        try:
            jira_log_script = self.workspace_dir / "jira_log.sh"
            if jira_log_script.exists():
                result = subprocess.run(
                    [str(jira_log_script), "log"],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print("✅ Jira log script completed")
                else:
                    print(f"⚠️  Jira log script exited with code {result.returncode}")
                return result.returncode == 0
            else:
                print("❌ jira_log.sh not found")
                return False
        except Exception as e:
            print(f"❌ Error running Jira log: {e}")
            return False
    
    def create_daily_log(self):
        """Create today's daily log"""
        try:
            create_log_script = self.workspace_dir / "create_daily_log.sh"
            if create_log_script.exists():
                result = subprocess.run(
                    [str(create_log_script)],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print("✅ Daily log created")
                return result.returncode == 0
            else:
                print("❌ create_daily_log.sh not found")
                return False
        except Exception as e:
            print(f"❌ Error creating daily log: {e}")
            return False
    
    def check_scheduled_prompts(self):
        """Check for scheduled prompt times"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        prompts = {
            self.morning_prompt: "🕛 Mid-day check: Have you logged your morning work to Jira?",
            self.afternoon_prompt: "🕓 Afternoon check: Time to log your afternoon work!",
            self.eod_prompt: "🕡 End of day: Don't forget to log all your work!"
        }
        
        for prompt_time, message in prompts.items():
            if current_time == prompt_time:
                print(f"⏰ Scheduled prompt at {prompt_time}")
                self.send_notification("Jira Work Log", message)
                return True
        
        return False
    
    def run_prompt_cycle(self):
        """Run one cycle of prompt checking"""
        if not self.is_work_hours():
            print(f"⏸️  Outside work hours ({datetime.now().strftime('%H:%M')})")
            return
        
        print(f"✅ In work hours ({datetime.now().strftime('%H:%M')})")
        
        # Check for scheduled prompts
        self.check_scheduled_prompts()
        
        # Optional: Random reminder (20% chance per cycle)
        import random
        if random.random() < 0.2:  # 20% chance
            reminder_messages = [
                "Remember to log your current work to Jira!",
                "Time for a quick Jira update?",
                "Don't forget to track your time in Jira!",
                "Quick check: Have you logged your recent work?"
            ]
            message = random.choice(reminder_messages)
            self.send_notification("Jira Reminder", message)
    
    def start(self, interval_minutes=30):
        """Start the prompt system"""
        print("🚀 Starting Manual Work Prompt System")
        print(f"   Work hours: {self.work_start_hour:02d}:00 - {self.work_end_hour:02d}:00")
        print(f"   Check interval: {interval_minutes} minutes")
        print(f"   Scheduled prompts: {self.morning_prompt}, {self.afternoon_prompt}, {self.eod_prompt}")
        print("=" * 50)
        
        self.running = True
        interval_seconds = interval_minutes * 60
        
        try:
            while self.running:
                self.run_prompt_cycle()
                
                # Sleep until next cycle
                for _ in range(interval_seconds):
                    if not self.running:
                        break
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print("\n🛑 Stopping prompt system...")
        finally:
            self.running = False
    
    def stop(self):
        """Stop the prompt system"""
        self.running = False
        print("🛑 Prompt system stopped")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Manual Work Prompt System")
    parser.add_argument('command', nargs='?', default='start',
                       choices=['start', 'stop', 'test', 'log', 'today'],
                       help='Command to run')
    parser.add_argument('--interval', type=int, default=30,
                       help='Check interval in minutes (default: 30)')
    
    args = parser.parse_args()
    
    system = WorkPromptSystem()
    
    if args.command == 'start':
        system.start(args.interval)
    
    elif args.command == 'stop':
        system.stop()
    
    elif args.command == 'test':
        print("🧪 System Test")
        print(f"Work hours: {system.is_work_hours()}")
        print(f"Current time: {datetime.now().strftime('%H:%M')}")
        
        # Test notification
        print("\nTesting notification...")
        system.send_notification("Test", "This is a test notification")
        
        # Test Jira connection
        print("\nTesting Jira connection...")
        from jira_tools import JiraClient
        jira = JiraClient()
        jira.test_connection()
    
    elif args.command == 'log':
        system.run_jira_log()
    
    elif args.command == 'today':
        system.create_daily_log()

if __name__ == "__main__":
    main()