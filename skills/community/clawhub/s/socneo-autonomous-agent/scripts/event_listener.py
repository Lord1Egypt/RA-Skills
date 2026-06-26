#!/usr/bin/env python3
"""
Event Listener - Perception Layer
Author: Socneo
Created with Claude Code
Version: 1.0.0

Multi-source event monitoring.
"""

import threading
import time
import os
from datetime import datetime
from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from enum import Enum

class EventType(Enum):
    SKILL_INSTALLED = "skill_installed"
    SKILL_UPDATED = "skill_updated"
    SKILL_REMOVED = "skill_removed"
    HIGH_CPU_USAGE = "high_cpu_usage"
    HIGH_MEMORY_USAGE = "high_memory_usage"
    FAILED_OPERATION = "failed_operation"
    USER_FEEDBACK = "user_feedback"
    FILE_MODIFIED = "file_modified"
    CONFIG_CHANGED = "config_changed"
    NEW_ERROR = "new_error"

@dataclass
class Event:
    """Event data structure."""
    event_type: EventType
    timestamp: datetime
    source: str
    data: Dict[str, Any]
    priority: str = "medium"

class FileSystemWatcher:
    """Monitor file system changes."""

    def __init__(self, watch_paths: List[str] = None):
        self.watch_paths = watch_paths or []
        self.file_states = {}
        self.is_monitoring = False
        self.callbacks = []

    def add_watch_path(self, path: str):
        """Add a path to monitor."""
        if os.path.exists(path) and path not in self.watch_paths:
            self.watch_paths.append(path)
            self._capture_initial_state(path)

    def _capture_initial_state(self, path: str):
        """Capture initial file state for comparison."""
        if os.path.isfile(path):
            stat = os.stat(path)
            self.file_states[path] = {
                'size': stat.st_size,
                'mtime': stat.st_mtime,
                'exists': True
            }
        else:
            self.file_states[path] = {'exists': False}

    def check_for_changes(self) -> List[Event]:
        """Check for file system changes and return events."""
        events = []

        for path in self.watch_paths:
            try:
                if os.path.exists(path):
                    if path not in self.file_states:
                        # New file detected
                        self._capture_initial_state(path)
                        events.append(Event(
                            event_type=EventType.FILE_MODIFIED,
                            timestamp=datetime.now(),
                            source="file_system",
                            data={'path': path, 'change_type': 'created'}
                        ))
                    else:
                        stat = os.stat(path)
                        old_state = self.file_states[path]

                        if (stat.st_size != old_state.get('size', 0) or
                            stat.st_mtime != old_state.get('mtime', 0)):
                            # File modified
                            events.append(Event(
                                event_type=EventType.FILE_MODIFIED,
                                timestamp=datetime.now(),
                                source="file_system",
                                data={'path': path, 'change_type': 'modified'}
                            ))
                            self._capture_initial_state(path)
                else:
                    if path in self.file_states and self.file_states[path].get('exists', False):
                        # File deleted
                        events.append(Event(
                            event_type=EventType.FILE_MODIFIED,
                            timestamp=datetime.now(),
                            source="file_system",
                            data={'path': path, 'change_type': 'deleted'}
                        ))
                        del self.file_states[path]

            except Exception as e:
                events.append(Event(
                    event_type=EventType.NEW_ERROR,
                    timestamp=datetime.now(),
                    source="file_system",
                    data={'path': path, 'error': str(e)}
                ))

        return events

class SkillUsageTracker:
    """Monitor skill usage patterns."""

    def __init__(self):
        self.skill_usage = {}
        self.skill_errors = {}
        self.installed_skills = set()

    def record_skill_usage(self, skill_name: str, operation: str, success: bool = True):
        """Record skill usage for analysis."""
        if skill_name not in self.skill_usage:
            self.skill_usage[skill_name] = {
                'total_uses': 0,
                'successful_uses': 0,
                'last_used': None,
                'operations': []
            }

        usage = self.skill_usage[skill_name]
        usage['total_uses'] += 1
        if success:
            usage['successful_uses'] += 1
        usage['last_used'] = datetime.now()
        usage['operations'].append({
            'operation': operation,
            'timestamp': datetime.now(),
            'success': success
        })

        # Keep only recent operations
        if len(usage['operations']) > 100:
            usage['operations'] = usage['operations'][-100:]

    def record_skill_installation(self, skill_name: str):
        """Record skill installation."""
        self.installed_skills.add(skill_name)
        return Event(
            event_type=EventType.SKILL_INSTALLED,
            timestamp=datetime.now(),
            source="skill_tracker",
            data={'skill_name': skill_name}
        )

    def record_skill_update(self, skill_name: str, version: str = None):
        """Record skill update."""
        return Event(
            event_type=EventType.SKILL_UPDATED,
            timestamp=datetime.now(),
            source="skill_tracker",
            data={'skill_name': skill_name, 'version': version}
        )

    def record_skill_error(self, skill_name: str, error: str):
        """Record skill error."""
        if skill_name not in self.skill_errors:
            self.skill_errors[skill_name] = []

        self.skill_errors[skill_name].append({
            'timestamp': datetime.now(),
            'error': error
        })

        # Keep only recent errors
        if len(self.skill_errors[skill_name]) > 50:
            self.skill_errors[skill_name] = self.skill_errors[skill_name][-50:]

        return Event(
            event_type=EventType.FAILED_OPERATION,
            timestamp=datetime.now(),
            source="skill_tracker",
            data={'skill_name': skill_name, 'error': error}
        )

class UserActivityMonitor:
    """Monitor user interaction patterns."""

    def __init__(self):
        self.user_sessions = []
        self.current_session_start = None
        self.interaction_count = 0

    def start_session(self):
        """Start a new user session."""
        if self.current_session_start is None:
            self.current_session_start = datetime.now()
            self.interaction_count = 0

    def record_interaction(self, interaction_type: str, details: Dict = None):
        """Record user interaction."""
        if self.current_session_start is None:
            self.start_session()

        self.interaction_count += 1
        return Event(
            event_type=EventType.USER_FEEDBACK,
            timestamp=datetime.now(),
            source="user_activity",
            data={
                'interaction_type': interaction_type,
                'session_duration': (datetime.now() - self.current_session_start).seconds,
                'interaction_count': self.interaction_count,
                'details': details or {}
            }
        )

    def end_session(self):
        """End current user session."""
        if self.current_session_start:
            session_data = {
                'start_time': self.current_session_start,
                'end_time': datetime.now(),
                'duration': (datetime.now() - self.current_session_start).seconds,
                'interactions': self.interaction_count
            }
            self.user_sessions.append(session_data)

            # Keep only recent sessions
            if len(self.user_sessions) > 100:
                self.user_sessions = self.user_sessions[-100:]

            self.current_session_start = None
            self.interaction_count = 0

            return session_data

class SystemMetricsCollector:
    """Collect and monitor system performance metrics."""

    def __init__(self, cpu_threshold: float = 80.0, memory_threshold: float = 85.0):
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.metrics_history = []

    def collect_metrics(self) -> Dict[str, Any]:
        """Collect current system metrics."""
        try:
            import psutil

            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            metrics = {
                'timestamp': datetime.now(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available': memory.available,
                'disk_percent': disk.percent,
                'processes': len(psutil.pids())
            }

            self.metrics_history.append(metrics)

            # Keep only recent metrics
            if len(self.metrics_history) > 1000:
                self.metrics_history = self.metrics_history[-1000:]

            return metrics

        except ImportError:
            # Fallback if psutil not available
            return {
                'timestamp': datetime.now(),
                'cpu_percent': 0,
                'memory_percent': 0,
                'disk_percent': 0,
                'processes': 0
            }

    def check_thresholds(self, metrics: Dict[str, Any]) -> List[Event]:
        """Check if metrics exceed thresholds and return events."""
        events = []

        if metrics['cpu_percent'] > self.cpu_threshold:
            events.append(Event(
                event_type=EventType.HIGH_CPU_USAGE,
                timestamp=datetime.now(),
                source="system_metrics",
                data={
                    'cpu_percent': metrics['cpu_percent'],
                    'threshold': self.cpu_threshold
                },
                priority="high"
            ))

        if metrics['memory_percent'] > self.memory_threshold:
            events.append(Event(
                event_type=EventType.HIGH_MEMORY_USAGE,
                timestamp=datetime.now(),
                source="system_metrics",
                data={
                    'memory_percent': metrics['memory_percent'],
                    'threshold': self.memory_threshold
                },
                priority="high"
            ))

        return events

class EventListener:
    """Main event listener that coordinates all monitoring components."""

    def __init__(self):
        self.file_watcher = FileSystemWatcher()
        self.skill_tracker = SkillUsageTracker()
        self.user_monitor = UserActivityMonitor()
        self.metrics_collector = SystemMetricsCollector()

        self.event_handlers = []
        self.is_monitoring = False

        # Default watch paths
        self._setup_default_watch_paths()

    def _setup_default_watch_paths(self):
        """Setup default paths to monitor."""
        default_paths = [
            "os.path.expanduser('~/.claude/skills')",
            "os.path.expanduser('~/.claude/config')",
            "os.path.expanduser('~/.claude/memory')"
        ]

        for path in default_paths:
            if os.path.exists(path):
                self.file_watcher.add_watch_path(path)

    def register_event_handler(self, handler: Callable[[Event], None]):
        """Register an event handler."""
        self.event_handlers.append(handler)

    def _process_events(self, events: List[Event]):
        """Process events through all registered handlers."""
        for event in events:
            for handler in self.event_handlers:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Error processing event {event.event_type}: {e}")

    def collect_all_events(self) -> List[Event]:
        """Collect events from all monitoring components."""
        all_events = []

        # File system events
        file_events = self.file_watcher.check_for_changes()
        all_events.extend(file_events)

        # System metrics events
        metrics = self.metrics_collector.collect_metrics()
        threshold_events = self.metrics_collector.check_thresholds(metrics)
        all_events.extend(threshold_events)

        return all_events

    def start_monitoring(self):
        """Start the event monitoring system."""
        if not self.is_monitoring:
            self.is_monitoring = True
            print("Event monitoring started")

    def stop_monitoring(self):
        """Stop the event monitoring system."""
        self.is_monitoring = False
        print("Event monitoring stopped")

    def get_status(self) -> Dict[str, Any]:
        """Get current event monitoring status."""
        return {
            'is_monitoring': self.is_monitoring,
            'watch_paths': self.file_watcher.watch_paths,
            'installed_skills': list(self.skill_tracker.installed_skills),
            'user_sessions': len(self.user_monitor.user_sessions),
            'metrics_history_length': len(self.metrics_collector.metrics_history),
            'event_handlers': len(self.event_handlers)
        }

def demo_event_listener():
    """Demonstrate the event listener system."""
    listener = EventListener()

    # Register event handler
    def sample_event_handler(event: Event):
        print(f"Event: {event.event_type.value} - {event.source} - {event.data}")

    listener.register_event_handler(sample_event_handler)

    print("Starting event listener demo...")
    listener.start_monitoring()

    # Simulate some events
    print("\nSimulating skill installation...")
    install_event = listener.skill_tracker.record_skill_installation("test-skill")
    listener._process_events([install_event])

    print("\nSimulating user interaction...")
    interaction_event = listener.user_monitor.record_interaction("skill_usage", {"skill": "test-skill"})
    listener._process_events([interaction_event])

    print("\nCollecting system events...")
    events = listener.collect_all_events()
    print(f"Collected {len(events)} events")

    print(f"\nSystem status: {listener.get_status()}")

    listener.stop_monitoring()

if __name__ == "__main__":
    demo_event_listener()
