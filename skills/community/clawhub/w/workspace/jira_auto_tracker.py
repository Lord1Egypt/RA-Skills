#!/usr/bin/env python3
"""
Jira Auto Tracker - OpenClaw Background Service
Runs continuously to prompt for work logging during business hours
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
import subprocess
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jira_tracker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class JiraAutoTracker:
    def __init__(self):
        self.workspace_dir = Path(__file__).parent
        self.config_file = self.workspace_dir / "jira_config.json"
        self.running = True
        
        # Tehran time work hours (8 AM - 7 PM)
        self.work_start_hour = 8
        self.work_end_hour = 19
        
        # Check interval in seconds (5 minutes)
        self.check_interval = 300
        
        # Last notification time to avoid spamming
        self.last_notification_time = {}
        
        logger.info("Jira Auto Tracker initialized")
        logger.info(f"Work hours: {self.work_start_hour}:00 - {self.work_end_hour}:00")
        logger.info(f"Check interval: {self.check_interval} seconds")
    
    def is_work_hours(self):
        """Check if current time is within work hours"""
        now = datetime.now()
        current_hour = now.hour
        
        # Check if within work hours
        in_hours = self.work_start_hour <= current_hour < self.work_end_hour
        
        # Check if weekday
        is_weekday = now.weekday() < 5  # 0-4 = Monday-Friday
        
        return in_hours and is_weekday
    
    def send_openclaw_notification(self, title, message):
        """Send notification through OpenClaw"""
        try:
            # This would use OpenClaw's notification system
            # For now, using macOS notifications as fallback
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(['osascript', '-e', script], capture_output=True)
            logger.info(f"Notification sent: {title} - {message}")
            return True
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            return False
    
    def check_scheduled_prompts(self):
        """Check for scheduled prompt times"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        # Scheduled prompts
        prompts = {
            "09:30": "Good morning! Time to plan your day and create your Jira work log.",
            "12:00": "Mid-day check: Have you logged your morning work to Jira?",
            "15:30": "Afternoon check: Don't forget to log your recent work!",
            "17:00": "End of day approaching: Time to log your afternoon work.",
            "18:30": "End of day: Make sure all work is logged to Jira!"
        }
        
        for prompt_time, message in prompts.items():
            if current_time == prompt_time:
                # Check if we already sent this notification today
                key = f"prompt_{prompt_time}"
                if key not in self.last_notification_time or \
                   (now - self.last_notification_time[key]).days >= 1:
                    
                    logger.info(f"Scheduled prompt at {prompt_time}: {message}")
                    self.send_openclaw_notification("Jira Work Log", message)
                    self.last_notification_time[key] = now
                    return True
        
        return False
    
    def check_random_reminder(self):
        """Send random reminder during work hours (low probability)"""
        import random
        
        # 10% chance per check during work hours
        if random.random() < 0.1 and self.is_work_hours():
            reminders = [
                "Quick reminder: Log your current work to Jira!",
                "Time for a Jira update?",
                "Don't forget to track your time!",
                "Jira check-in: Have you logged recent work?"
            ]
            
            message = random.choice(reminders)
            key = "random_reminder"
            now = datetime.now()
            
            # Only send once per hour
            if key not in self.last_notification_time or \
               (now - self.last_notification_time[key]).seconds >= 3600:
                
                logger.info(f"Random reminder: {message}")
                self.send_openclaw_notification("Jira Reminder", message)
                self.last_notification_time[key] = now
                return True
        
        return False
    
    def run_daily_startup(self):
        """Run daily startup tasks at beginning of work day"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        # Check if it's start of work day (8:00-8:30)
        if current_time >= "08:00" and current_time <= "08:30":
            key = "daily_startup"
            
            # Only run once per day
            if key not in self.last_notification_time or \
               (now - self.last_notification_time[key]).days >= 1:
                
                logger.info("Running daily startup tasks")
                
                # Create daily log
                create_log_script = self.workspace_dir / "create_daily_log.sh"
                if create_log_script.exists():
                    try:
                        result = subprocess.run(
                            [str(create_log_script)],
                            capture_output=True,
                            text=True
                        )
                        if result.returncode == 0:
                            logger.info("Daily log created successfully")
                        else:
                            logger.error(f"Failed to create daily log: {result.stderr}")
                    except Exception as e:
                        logger.error(f"Error creating daily log: {e}")
                
                # Send startup notification
                self.send_openclaw_notification(
                    "Jira Work Day Start",
                    "Good morning! Your daily work log has been created. Remember to log your work throughout the day."
                )
                
                self.last_notification_time[key] = now
                return True
        
        return False
    
    def run_check_cycle(self):
        """Run one cycle of checks"""
        try:
            # Run daily startup tasks
            self.run_daily_startup()
            
            # Check scheduled prompts
            self.check_scheduled_prompts()
            
            # Check random reminders
            self.check_random_reminder()
            
            # Log status
            if self.is_work_hours():
                status = "IN WORK HOURS"
            else:
                status = "OUTSIDE WORK HOURS"
            
            logger.debug(f"Check cycle completed - {status}")
            return True
            
        except Exception as e:
            logger.error(f"Error in check cycle: {e}", exc_info=True)
            return False
    
    def start(self):
        """Start the auto tracker"""
        logger.info("🚀 Starting Jira Auto Tracker")
        logger.info("This will run continuously in the background")
        logger.info("Press Ctrl+C to stop")
        
        try:
            while self.running:
                # Run check cycle
                self.run_check_cycle()
                
                # Sleep until next check
                for _ in range(self.check_interval):
                    if not self.running:
                        break
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            logger.info("\n🛑 Stopping Jira Auto Tracker...")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
        finally:
            self.running = False
            logger.info("Jira Auto Tracker stopped")
    
    def stop(self):
        """Stop the auto tracker"""
        self.running = False
        logger.info("Stopping signal received")

def main():
    tracker = JiraAutoTracker()
    tracker.start()

if __name__ == "__main__":
    main()