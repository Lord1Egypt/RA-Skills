#!/usr/bin/env python3
"""
State Awareness - Perception Layer
Author: Socneo
Created with Claude Code
Version: 1.0.0

System state capture and analysis.
"""

import os
import json
import psutil
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class SystemState:
    """Represents the current state of the system."""
    timestamp: datetime
    active_skills: List[str]
    resource_usage: Dict[str, float]
    recent_errors: List[Dict]
    user_patterns: Dict[str, Any]
    skill_performance: Dict[str, Any]
    configuration_status: Dict[str, Any]
    memory_usage: Dict[str, Any]

class StateAwareness:
    """Comprehensive system state awareness engine."""

    def __init__(self, skills_path: str = None, memory_path: str = None):
        self.skills_path = skills_path or "os.path.expanduser('~/.claude/skills')"
        self.memory_path = memory_path or "os.path.expanduser('~/.claude/memory')"
        self.state_history = []
        self.max_history_size = 1000
        self.current_state = None

    def capture_system_state(self) -> SystemState:
        """Capture comprehensive system state."""
        state = SystemState(
            timestamp=datetime.now(),
            active_skills=self._get_active_skills(),
            resource_usage=self._get_resource_metrics(),
            recent_errors=self._get_recent_errors(),
            user_patterns=self._analyze_user_patterns(),
            skill_performance=self._get_skill_performance(),
            configuration_status=self._get_configuration_status(),
            memory_usage=self._get_memory_usage()
        )

        self.current_state = state
        self.state_history.append(state)

        # Maintain history size limit
        if len(self.state_history) > self.max_history_size:
            self.state_history = self.state_history[-self.max_history_size:]

        return state

    def _get_active_skills(self) -> List[str]:
        """Get list of currently active/installed skills."""
        active_skills = []

        try:
            if os.path.exists(self.skills_path):
                for item in os.listdir(self.skills_path):
                    skill_path = os.path.join(self.skills_path, item)
                    if os.path.isdir(skill_path):
                        # Check if it's a valid skill directory
                        skill_md_path = os.path.join(skill_path, "SKILL.md")
                        if os.path.exists(skill_md_path):
                            active_skills.append(item)
        except Exception as e:
            print(f"Error getting active skills: {e}")

        return active_skills

    def _get_resource_metrics(self) -> Dict[str, float]:
        """Get current system resource usage metrics."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': memory.available / (1024**3),
                'disk_percent': disk.percent,
                'disk_free_gb': disk.free / (1024**3),
                'process_count': len(psutil.pids())
            }
        except Exception as e:
            print(f"Error getting resource metrics: {e}")
            return {
                'cpu_percent': 0,
                'memory_percent': 0,
                'memory_available_gb': 0,
                'disk_percent': 0,
                'disk_free_gb': 0,
                'process_count': 0
            }

    def _get_recent_errors(self, hours: int = 24) -> List[Dict]:
        """Get recent system errors from logs."""
        errors = []
        cutoff_time = datetime.now() - timedelta(hours=hours)

        # Look for error logs in common locations
        log_locations = [
            "os.path.expanduser('~/.claude/logs')",
            "/var/log",
            "./logs"
        ]

        for log_dir in log_locations:
            if os.path.exists(log_dir):
                try:
                    for log_file in os.listdir(log_dir):
                        if log_file.endswith('.log'):
                            file_path = os.path.join(log_dir, log_file)
                            file_errors = self._parse_error_log(file_path, cutoff_time)
                            errors.extend(file_errors)
                except Exception as e:
                    print(f"Error reading log directory {log_dir}: {e}")

        return errors

    def _parse_error_log(self, file_path: str, cutoff_time: datetime) -> List[Dict]:
        """Parse error log file for recent errors."""
        errors = []

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    # Simple error detection - look for common error keywords
                    if any(keyword in line.lower() for keyword in ['error', 'exception', 'failed', 'critical']):
                        # Try to extract timestamp and error details
                        error_entry = {
                            'timestamp': self._extract_timestamp(line) or datetime.now(),
                            'source': file_path,
                            'message': line.strip(),
                            'severity': self._determine_severity(line)
                        }

                        if error_entry['timestamp'] > cutoff_time:
                            errors.append(error_entry)

        except Exception as e:
            print(f"Error parsing log file {file_path}: {e}")

        return errors

    def _extract_timestamp(self, log_line: str) -> Optional[datetime]:
        """Extract timestamp from log line."""
        # Simple timestamp extraction - can be enhanced based on log format
        import re

        # Common timestamp patterns
        patterns = [
            r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',
            r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})',
            r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})'
        ]

        for pattern in patterns:
            match = re.search(pattern, log_line)
            if match:
                try:
                    return datetime.fromisoformat(match.group(1).replace('T', ' '))
                except:
                    continue

        return None

    def _determine_severity(self, log_line: str) -> str:
        """Determine error severity from log line."""
        line_lower = log_line.lower()

        if any(word in line_lower for word in ['critical', 'fatal', 'emergency']):
            return 'critical'
        elif any(word in line_lower for word in ['error', 'exception', 'failed']):
            return 'error'
        elif any(word in line_lower for word in ['warning', 'warn']):
            return 'warning'
        else:
            return 'info'

    def _analyze_user_patterns(self) -> Dict[str, Any]:
        """Analyze user interaction patterns."""
        patterns = {
            'recent_activity': self._get_recent_user_activity(),
            'preferred_skills': self._get_preferred_skills(),
            'usage_frequency': self._get_usage_frequency(),
            'session_patterns': self._get_session_patterns()
        }

        return patterns

    def _get_recent_user_activity(self) -> List[Dict]:
        """Get recent user activity patterns."""
        # This would integrate with actual user activity tracking
        # For now, return sample data
        return [
            {
                'timestamp': datetime.now() - timedelta(minutes=30),
                'activity': 'skill_usage',
                'skill': 'autonomous-agent'
            },
            {
                'timestamp': datetime.now() - timedelta(hours=2),
                'activity': 'configuration_change',
                'target': 'settings.json'
            }
        ]

    def _get_preferred_skills(self) -> Dict[str, int]:
        """Get user's preferred skills based on usage frequency."""
        # This would analyze actual skill usage data
        # For now, return sample preferences
        return {
            'ima-skill': 15,
            'skill-finder': 12,
            'autonomous-agent': 8,
            'config-manager': 6
        }

    def _get_usage_frequency(self) -> Dict[str, str]:
        """Get usage frequency patterns."""
        return {
            'daily_sessions': '3-5',
            'peak_hours': ['09:00-11:00', '14:00-16:00', '20:00-22:00'],
            'average_session_duration': '45 minutes'
        }

    def _get_session_patterns(self) -> Dict[str, Any]:
        """Get user session patterns."""
        return {
            'average_sessions_per_day': 4,
            'average_session_length_minutes': 35,
            'most_active_day': 'Tuesday',
            'preferred_working_hours': '09:00-17:00'
        }

    def _get_skill_performance(self) -> Dict[str, Any]:
        """Get performance metrics for installed skills."""
        performance = {}

        for skill_name in self._get_active_skills():
            # This would analyze actual skill performance data
            # For now, return sample performance metrics
            performance[skill_name] = {
                'execution_time_avg': 2.5,
                'success_rate': 0.95,
                'last_execution': datetime.now() - timedelta(hours=1),
                'total_executions': 45,
                'error_count': 2
            }

        return performance

    def _get_configuration_status(self) -> Dict[str, Any]:
        """Get configuration files status."""
        config_status = {}

        config_files = [
            "os.path.join(os.path.expanduser('~/.claude'), 'settings.json')",
            "os.path.join(os.path.expanduser('~/.claude'), 'settings.local.json')"
        ]

        for config_file in config_files:
            if os.path.exists(config_file):
                try:
                    stat = os.stat(config_file)
                    with open(config_file, 'r') as f:
                        config_data = json.load(f)

                    config_status[config_file] = {
                        'exists': True,
                        'last_modified': datetime.fromtimestamp(stat.st_mtime),
                        'size_bytes': stat.st_size,
                        'valid_json': True,
                        'key_count': len(config_data)
                    }
                except Exception as e:
                    config_status[config_file] = {
                        'exists': True,
                        'last_modified': datetime.fromtimestamp(stat.st_mtime),
                        'size_bytes': stat.st_size,
                        'valid_json': False,
                        'error': str(e)
                    }
            else:
                config_status[config_file] = {
                    'exists': False
                }

        return config_status

    def _get_memory_usage(self) -> Dict[str, Any]:
        """Get memory system usage."""
        memory_usage = {}

        if os.path.exists(self.memory_path):
            try:
                total_size = 0
                file_count = 0
                recent_files = []

                for root, dirs, files in os.walk(self.memory_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            file_size = os.path.getsize(file_path)
                            total_size += file_size
                            file_count += 1

                            # Track recent files
                            mtime = os.path.getmtime(file_path)
                            if datetime.fromtimestamp(mtime) > datetime.now() - timedelta(days=7):
                                recent_files.append({
                                    'path': file_path,
                                    'size': file_size,
                                    'modified': datetime.fromtimestamp(mtime)
                                })
                        except Exception:
                            pass

                memory_usage = {
                    'total_size_mb': total_size / (1024 * 1024),
                    'file_count': file_count,
                    'recent_files_count': len(recent_files),
                    'recent_files': recent_files[:10]  # Top 10 recent files
                }

            except Exception as e:
                print(f"Error analyzing memory usage: {e}")
                memory_usage = {
                    'total_size_mb': 0,
                    'file_count': 0,
                    'recent_files_count': 0,
                    'recent_files': []
                }

        return memory_usage

    def detect_anomalies(self) -> List[Dict]:
        """Detect anomalies in current system state."""
        if not self.current_state or len(self.state_history) < 5:
            return []

        anomalies = []

        # Check for resource usage anomalies
        current_resources = self.current_state.resource_usage
        if current_resources['cpu_percent'] > 90:
            anomalies.append({
                'type': 'high_cpu_usage',
                'severity': 'warning',
                'value': current_resources['cpu_percent'],
                'threshold': 90
            })

        if current_resources['memory_percent'] > 90:
            anomalies.append({
                'type': 'high_memory_usage',
                'severity': 'warning',
                'value': current_resources['memory_percent'],
                'threshold': 90
            })

        # Check for error spikes
        recent_errors = len(self.current_state.recent_errors)
        if recent_errors > 10:
            anomalies.append({
                'type': 'error_spike',
                'severity': 'error',
                'error_count': recent_errors,
                'threshold': 10
            })

        # Check for configuration issues
        for config_file, status in self.current_state.configuration_status.items():
            if status.get('exists') and not status.get('valid_json'):
                anomalies.append({
                    'type': 'invalid_configuration',
                    'severity': 'error',
                    'file': config_file,
                    'error': status.get('error')
                })

        return anomalies

    def get_state_summary(self) -> Dict[str, Any]:
        """Get a summary of current system state."""
        if not self.current_state:
            return {'status': 'no_data'}

        return {
            'timestamp': self.current_state.timestamp.isoformat(),
            'active_skills_count': len(self.current_state.active_skills),
            'cpu_usage': self.current_state.resource_usage.get('cpu_percent', 0),
            'memory_usage': self.current_state.resource_usage.get('memory_percent', 0),
            'recent_errors': len(self.current_state.recent_errors),
            'anomalies': self.detect_anomalies(),
            'system_health': self._calculate_system_health()
        }

    def _calculate_system_health(self) -> str:
        """Calculate overall system health score."""
        if not self.current_state:
            return 'unknown'

        health_score = 100

        # Deduct points for resource issues
        cpu_usage = self.current_state.resource_usage.get('cpu_percent', 0)
        memory_usage = self.current_state.resource_usage.get('memory_percent', 0)

        if cpu_usage > 80:
            health_score -= 20
        elif cpu_usage > 60:
            health_score -= 10

        if memory_usage > 80:
            health_score -= 20
        elif memory_usage > 60:
            health_score -= 10

        # Deduct points for errors
        error_count = len(self.current_state.recent_errors)
        if error_count > 10:
            health_score -= 30
        elif error_count > 5:
            health_score -= 15

        # Deduct points for configuration issues
        for status in self.current_state.configuration_status.values():
            if status.get('exists') and not status.get('valid_json'):
                health_score -= 25

        if health_score >= 80:
            return 'excellent'
        elif health_score >= 60:
            return 'good'
        elif health_score >= 40:
            return 'fair'
        else:
            return 'poor'

def demo_state_awareness():
    """Demonstrate the state awareness system."""
    awareness = StateAwareness()

    print("Capturing system state...")
    state = awareness.capture_system_state()

    print(f"\nSystem State Captured:")
    print(f"- Timestamp: {state.timestamp}")
    print(f"- Active Skills: {len(state.active_skills)}")
    print(f"- CPU Usage: {state.resource_usage.get('cpu_percent', 0)}%")
    print(f"- Memory Usage: {state.resource_usage.get('memory_percent', 0)}%")
    print(f"- Recent Errors: {len(state.recent_errors)}")

    print(f"\nSystem Health: {awareness._calculate_system_health()}")

    anomalies = awareness.detect_anomalies()
    if anomalies:
        print(f"\nDetected Anomalies:")
        for anomaly in anomalies:
            print(f"- {anomaly['type']}: {anomaly}")

    summary = awareness.get_state_summary()
    print(f"\nState Summary: {summary}")

if __name__ == "__main__":
    demo_state_awareness()
