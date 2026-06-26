#!/usr/bin/env python3
"""
Smart Heartbeat - Perception Layer
Author: Socneo
Created with Claude Code
Version: 1.0.0

Adaptive monitoring heartbeat.
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Callable
from enum import Enum

class ActivityLevel(Enum):
    LOW = "low_activity"
    NORMAL = "normal"
    HIGH = "high_activity"

class SmartHeartbeat:
    def __init__(self, base_interval: int = 300):
        """Initialize the smart heartbeat system.

        Args:
            base_interval: Base heartbeat interval in seconds (default: 5 minutes)
        """
        self.base_interval = base_interval
        self.adaptive_intervals = {
            ActivityLevel.HIGH: 60,      # 1 minute for high activity
            ActivityLevel.NORMAL: 300,   # 5 minutes for normal
            ActivityLevel.LOW: 900       # 15 minutes for low activity
        }
        self.current_activity_level = ActivityLevel.NORMAL
        self.is_running = False
        self.heartbeat_thread = None

        # Activity tracking
        self.recent_operations = []
        self.max_tracked_operations = 50

        # Event callbacks
        self.callbacks = []

    def detect_activity_level(self) -> ActivityLevel:
        """Analyze recent activity to determine current activity level."""
        now = datetime.now()
        thirty_minutes_ago = now - timedelta(minutes=30)

        # Count operations in last 30 minutes
        recent_ops = [op for op in self.recent_operations
                     if op['timestamp'] > thirty_minutes_ago]

        operation_count = len(recent_ops)

        # Determine activity level based on operation frequency
        if operation_count > 10:
            self.current_activity_level = ActivityLevel.HIGH
        elif operation_count < 2:
            self.current_activity_level = ActivityLevel.LOW
        else:
            self.current_activity_level = ActivityLevel.NORMAL

        return self.current_activity_level

    def get_current_interval(self) -> int:
        """Get the current heartbeat interval based on activity level."""
        self.detect_activity_level()
        return self.adaptive_intervals[self.current_activity_level]

    def record_operation(self, operation_type: str, details: Dict = None):
        """Record a system operation for activity analysis."""
        operation = {
            'type': operation_type,
            'timestamp': datetime.now(),
            'details': details or {}
        }

        self.recent_operations.append(operation)

        # Keep only recent operations
        if len(self.recent_operations) > self.max_tracked_operations:
            self.recent_operations = self.recent_operations[-self.max_tracked_operations:]

    def register_callback(self, callback: Callable):
        """Register a callback function to be called on heartbeat."""
        self.callbacks.append(callback)

    def _heartbeat_loop(self):
        """Main heartbeat loop."""
        while self.is_running:
            try:
                # Get current interval
                interval = self.get_current_interval()

                # Execute callbacks
                for callback in self.callbacks:
                    try:
                        callback({
                            'timestamp': datetime.now(),
                            'activity_level': self.current_activity_level.value,
                            'interval': interval,
                            'recent_operations': len(self.recent_operations)
                        })
                    except Exception as e:
                        print(f"Error in heartbeat callback: {e}")

                # Sleep for the adaptive interval
                time.sleep(interval)

            except Exception as e:
                print(f"Error in heartbeat loop: {e}")
                time.sleep(60)  # Fallback sleep

    def start(self):
        """Start the heartbeat system."""
        if not self.is_running:
            self.is_running = True
            self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
            self.heartbeat_thread.start()
            print(f"Smart heartbeat started with adaptive intervals")

    def stop(self):
        """Stop the heartbeat system."""
        self.is_running = False
        if self.heartbeat_thread:
            self.heartbeat_thread.join(timeout=5)
        print("Smart heartbeat stopped")

    def get_status(self) -> Dict:
        """Get current heartbeat system status."""
        return {
            'is_running': self.is_running,
            'activity_level': self.current_activity_level.value,
            'current_interval': self.get_current_interval(),
            'recent_operations_count': len(self.recent_operations),
            'registered_callbacks': len(self.callbacks)
        }

def demo_smart_heartbeat():
    """Demonstrate the smart heartbeat system."""
    heartbeat = SmartHeartbeat()

    # Register a sample callback
    def sample_callback(heartbeat_data):
        print(f"Heartbeat: {heartbeat_data['activity_level']} - "
              f"Interval: {heartbeat_data['interval']}s - "
              f"Ops: {heartbeat_data['recent_operations']}")

    heartbeat.register_callback(sample_callback)

    # Simulate activity
    print("Starting smart heartbeat demo...")
    heartbeat.start()

    # Simulate different activity levels
    print("\nSimulating low activity...")
    time.sleep(10)

    print("\nSimulating normal activity...")
    for i in range(5):
        heartbeat.record_operation(f"normal_op_{i}")
        time.sleep(1)

    print("\nSimulating high activity...")
    for i in range(15):
        heartbeat.record_operation(f"high_op_{i}")
        time.sleep(0.5)

    print("\nSimulating low activity again...")
    time.sleep(20)

    # Show final status
    print(f"\nFinal status: {heartbeat.get_status()}")

    heartbeat.stop()

if __name__ == "__main__":
    demo_smart_heartbeat()
