#!/usr/bin/env python3
"""
Jira Work Log TaskFlow
Persistent background task that survives session timeouts
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
import subprocess
import logging
from pathlib import Path

# Add OpenClaw skill path
sys.path.append('/Users/alighotbizadeh/.nvm/versions/node/v24.15.0/lib/node_modules/openclaw/skills')

try:
    # Try to import TaskFlow runtime
    import taskflow
    TASKFLOW_AVAILABLE = True
except ImportError:
    TASKFLOW_AVAILABLE = False
    print("⚠️ TaskFlow not available, running in standalone mode")

class JiraTaskFlow:
    def __init__(self):
        self.workspace_dir = Path(__file__).parent
        self.config_file = self.workspace_dir / "jira_config.json"
        
        # Work hours (8 AM - 7 PM Tehran time)
        self.work_start_hour = 8
        self.work_end_hour = 19
        
        # State file for persistence
        self.state_file = self.workspace_dir / ".jira_taskflow_state.json"
        self.state = self.load_state()
        
        # Setup logging
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging for TaskFlow"""
        log_file = self.workspace_dir / "taskflow_jira.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("JiraTaskFlow")
        
    def load_state(self):
        """Load persistent state"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "last_daily_log": None,
            "last_notification": {},
            "last_health_check": None
        }
    
    def save_state(self):
        """Save persistent state"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save state: {e}")
    
    def is_work_hours(self):
        """Check if current time is within work hours"""
        now = datetime.now()
        current_hour = now.hour
        is_weekday = now.weekday() < 5  # Monday-Friday
        return self.work_start_hour <= current_hour < self.work_end_hour and is_weekday
    
    def send_notification(self, title, message):
        """Send macOS notification"""
        try:
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(['osascript', '-e', script], capture_output=True)
            self.logger.info(f"Notification sent: {title}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")
            return False
    
    def create_daily_log(self):
        """Create today's daily log if not already created"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if self.state.get("last_daily_log") == today:
            self.logger.info(f"Daily log already created for {today}")
            return False
        
        try:
            create_log_script = self.workspace_dir / "create_daily_log.sh"
            if create_log_script.exists():
                result = subprocess.run(
                    [str(create_log_script)],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    self.state["last_daily_log"] = today
                    self.save_state()
                    self.logger.info(f"Daily log created for {today}")
                    return True
                else:
                    self.logger.error(f"Failed to create daily log: {result.stderr}")
                    return False
            else:
                self.logger.error("create_daily_log.sh not found")
                return False
        except Exception as e:
            self.logger.error(f"Error creating daily log: {e}")
            return False
    
    def check_scheduled_tasks(self):
        """Check and execute scheduled tasks"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        today = now.strftime("%Y-%m-%d")
        
        # Scheduled tasks with their times
        tasks = {
            "08:00": {"type": "daily_log", "message": "Creating daily work log"},
            "09:30": {"type": "morning_reminder", "message": "Good morning! Time to plan your day and log work to Jira."},
            "12:00": {"type": "midday_check", "message": "Mid-day check: Have you logged your morning work to Jira?"},
            "15:30": {"type": "afternoon_check", "message": "Afternoon check: Don't forget to log your recent work!"},
            "17:00": {"type": "eod_approaching", "message": "End of day approaching: Time to log your afternoon work."},
            "18:30": {"type": "final_reminder", "message": "End of day: Make sure all work is logged to Jira!"}
        }
        
        for task_time, task_info in tasks.items():
            if current_time == task_time:
                task_key = f"{today}_{task_info['type']}"
                
                # Check if already executed today
                if task_key not in self.state.get("executed_tasks", {}):
                    self.logger.info(f"Executing scheduled task: {task_info['type']} at {task_time}")
                    
                    # Execute task
                    if task_info["type"] == "daily_log":
                        self.create_daily_log()
                    else:
                        self.send_notification("Jira Work Log", task_info["message"])
                    
                    # Mark as executed
                    if "executed_tasks" not in self.state:
                        self.state["executed_tasks"] = {}
                    self.state["executed_tasks"][task_key] = now.isoformat()
                    self.save_state()
                    
                    return True
        
        return False
    
    def health_check(self):
        """Perform health check of Jira connection"""
        try:
            # Import Jira client
            sys.path.append(str(self.workspace_dir))
            from jira_tools import JiraClient
            
            jira = JiraClient()
            if jira.test_connection():
                self.logger.info("Health check: Jira connection OK")
                self.state["last_health_check"] = datetime.now().isoformat()
                self.save_state()
                return True
            else:
                self.logger.warning("Health check: Jira connection failed")
                return False
        except Exception as e:
            self.logger.error(f"Health check error: {e}")
            return False
    
    def run_cycle(self):
        """Run one cycle of checks"""
        try:
            # Clear old executed tasks (older than 1 day)
            self.cleanup_old_tasks()
            
            # Check scheduled tasks
            self.check_scheduled_tasks()
            
            # Health check at 9:00
            now = datetime.now()
            if now.strftime("%H:%M") == "09:00":
                if self.state.get("last_health_check") != now.strftime("%Y-%m-%d"):
                    self.health_check()
            
            # Random reminders during work hours
            if self.is_work_hours():
                self.send_random_reminder()
            
            self.logger.debug(f"Cycle completed at {now.isoformat()}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error in run_cycle: {e}", exc_info=True)
            return False
    
    def cleanup_old_tasks(self):
        """Clean up tasks older than 1 day"""
        now = datetime.now()
        cutoff = now - timedelta(days=1)
        
        if "executed_tasks" in self.state:
            # Remove tasks older than 1 day
            self.state["executed_tasks"] = {
                k: v for k, v in self.state["executed_tasks"].items()
                if datetime.fromisoformat(v) > cutoff
            }
            self.save_state()
    
    def send_random_reminder(self):
        """Send random reminder during work hours"""
        import random
        
        # 5% chance per cycle
        if random.random() < 0.05:
            reminders = [
                "Quick reminder: Log your current work to Jira!",
                "Time for a Jira update?",
                "Don't forget to track your time!",
                "Jira check-in: Have you logged recent work?"
            ]
            
            message = random.choice(reminders)
            key = f"random_{datetime.now().strftime('%Y-%m-%d_%H')}"
            
            # Only send once per hour
            if key not in self.state.get("random_reminders", {}):
                self.send_notification("Jira Reminder", message)
                
                if "random_reminders" not in self.state:
                    self.state["random_reminders"] = {}
                self.state["random_reminders"][key] = datetime.now().isoformat()
                self.save_state()
    
    def run_as_taskflow(self):
        """Run as TaskFlow job"""
        if not TASKFLOW_AVAILABLE:
            self.logger.error("TaskFlow not available")
            return self.run_standalone()
        
        try:
            # This would integrate with OpenClaw TaskFlow
            # For now, run in standalone mode
            return self.run_standalone()
        except Exception as e:
            self.logger.error(f"TaskFlow error: {e}")
            return self.run_standalone()
    
    def run_standalone(self):
        """Run in standalone mode (for testing)"""
        self.logger.info("Starting Jira TaskFlow in standalone mode")
        
        try:
            while True:
                self.run_cycle()
                time.sleep(300)  # Check every 5 minutes
                
        except KeyboardInterrupt:
            self.logger.info("Stopped by user")
        except Exception as e:
            self.logger.error(f"Fatal error: {e}", exc_info=True)
            return False
        
        return True

def main():
    """Main entry point"""
    taskflow = JiraTaskFlow()
    
    # Check if running as TaskFlow or standalone
    if len(sys.argv) > 1 and sys.argv[1] == "--taskflow":
        taskflow.run_as_taskflow()
    else:
        taskflow.run_standalone()

if __name__ == "__main__":
    main()