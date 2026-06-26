#!/usr/bin/env python3
"""
Progress Tracking - Execution Layer
Author: Socneo
Created with Claude Code
Version: 1.0.0

Task execution progress monitoring.
"""

import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import uuid

class ProgressStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PAUSED = "paused"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ProgressType(Enum):
    TASK = "task"
    SUBTASK = "subtask"
    PHASE = "phase"
    MILESTONE = "milestone"

@dataclass
class ProgressCheckpoint:
    """Represents a progress checkpoint."""
    id: str
    name: str
    description: str
    target_value: float
    current_value: float = 0.0
    unit: str = ""
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProgressTracker:
    """Represents a progress tracking instance."""
    id: str
    name: str
    total_work: float
    completed_work: float = 0.0
    status: ProgressStatus = ProgressStatus.NOT_STARTED
    progress_type: ProgressType = ProgressType.TASK
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_completion: Optional[datetime] = None
    checkpoints: List[ProgressCheckpoint] = field(default_factory=list)
    subtasks: List[str] = field(default_factory=list)  # IDs of subtask trackers
    parent_task: Optional[str] = None
    progress_callbacks: List[Callable] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def progress_percentage(self) -> float:
        """Calculate progress as percentage."""
        if self.total_work == 0:
            return 0.0
        return min((self.completed_work / self.total_work) * 100, 100.0)

    @property
    def is_completed(self) -> bool:
        """Check if progress is completed."""
        return self.status == ProgressStatus.COMPLETED or self.progress_percentage >= 100.0

    @property
    def elapsed_time(self) -> Optional[timedelta]:
        """Get elapsed time since start."""
        if not self.started_at:
            return None
        end_time = self.completed_at or datetime.now()
        return end_time - self.started_at

    @property
    def estimated_remaining_time(self) -> Optional[timedelta]:
        """Estimate remaining time to completion."""
        if not self.started_at or self.completed_work == 0:
            return None

        elapsed = self.elapsed_time
        if not elapsed:
            return None

        # Calculate rate of progress
        elapsed_seconds = elapsed.total_seconds()
        work_rate = self.completed_work / elapsed_seconds if elapsed_seconds > 0 else 0

        if work_rate == 0:
            return None

        remaining_work = self.total_work - self.completed_work
        estimated_seconds = remaining_work / work_rate

        return timedelta(seconds=estimated_seconds)

class ProgressTrackingSystem:
    """Advanced progress tracking system with real-time monitoring and reporting."""

    def __init__(self):
        self.trackers: Dict[str, ProgressTracker] = {}
        self.active_trackers: Dict[str, ProgressTracker] = {}
        self.completed_trackers: Dict[str, ProgressTracker] = {}
        self.tracking_lock = threading.RLock()
        self.update_callbacks: List[Callable] = []
        self.notification_thresholds = [25, 50, 75, 90, 100]  # Percentage thresholds
        self.notified_thresholds: Dict[str, set] = {}  # Track which thresholds have been notified

    def create_tracker(self, name: str, total_work: float, progress_type: ProgressType = ProgressType.TASK,
                      parent_task: Optional[str] = None, metadata: Dict[str, Any] = None) -> str:
        """Create a new progress tracker."""

        tracker_id = str(uuid.uuid4())
        tracker = ProgressTracker(
            id=tracker_id,
            name=name,
            total_work=total_work,
            progress_type=progress_type,
            parent_task=parent_task,
            metadata=metadata or {}
        )

        with self.tracking_lock:
            self.trackers[tracker_id] = tracker
            self.notified_thresholds[tracker_id] = set()

        return tracker_id

    def start_tracking(self, tracker_id: str) -> bool:
        """Start tracking progress for a task."""

        with self.tracking_lock:
            if tracker_id not in self.trackers:
                return False

            tracker = self.trackers[tracker_id]
            tracker.status = ProgressStatus.IN_PROGRESS
            tracker.started_at = datetime.now()

            # Add to active trackers
            self.active_trackers[tracker_id] = tracker

            # Remove from completed if it was there
            if tracker_id in self.completed_trackers:
                del self.completed_trackers[tracker_id]

            self._notify_progress_update(tracker, "started")
            return True

    def update_progress(self, tracker_id: str, completed_work: float, checkpoint_name: Optional[str] = None,
                       checkpoint_data: Optional[Dict[str, Any]] = None) -> bool:
        """Update progress for a tracker."""

        with self.tracking_lock:
            if tracker_id not in self.trackers:
                return False

            tracker = self.trackers[tracker_id]
            old_progress = tracker.progress_percentage

            # Update completed work
            tracker.completed_work = min(completed_work, tracker.total_work)

            # Check if completed
            if tracker.progress_percentage >= 100.0:
                self._mark_completed(tracker_id)

            # Handle checkpoint if provided
            if checkpoint_name:
                self._update_checkpoint(tracker_id, checkpoint_name, checkpoint_data)

            # Check notification thresholds
            new_progress = tracker.progress_percentage
            self._check_notification_thresholds(tracker_id, old_progress, new_progress)

            # Notify callbacks
            self._notify_progress_update(tracker, "progress_updated")

            # Update estimated completion time
            self._update_estimated_completion(tracker)

            return True

    def add_checkpoint(self, tracker_id: str, name: str, description: str, target_value: float,
                      unit: str = "", metadata: Dict[str, Any] = None) -> bool:
        """Add a checkpoint to a tracker."""

        with self.tracking_lock:
            if tracker_id not in self.trackers:
                return False

            tracker = self.trackers[tracker_id]
            checkpoint = ProgressCheckpoint(
                id=str(uuid.uuid4()),
                name=name,
                description=description,
                target_value=target_value,
                unit=unit,
                metadata=metadata or {}
            )
            tracker.checkpoints.append(checkpoint)
            return True

    def _update_checkpoint(self, tracker_id: str, checkpoint_name: str, data: Optional[Dict[str, Any]]):
        """Update a specific checkpoint."""

        tracker = self.trackers[tracker_id]
        for checkpoint in tracker.checkpoints:
            if checkpoint.name == checkpoint_name:
                if data and 'current_value' in data:
                    checkpoint.current_value = data['current_value']
                if data and 'completed' in data and data['completed']:
                    checkpoint.completed_at = datetime.now()
                break

    def _mark_completed(self, tracker_id: str):
        """Mark a tracker as completed."""

        tracker = self.trackers[tracker_id]
        tracker.status = ProgressStatus.COMPLETED
        tracker.completed_at = datetime.now()
        tracker.completed_work = tracker.total_work

        # Move from active to completed
        if tracker_id in self.active_trackers:
            del self.active_trackers[tracker_id]
        self.completed_trackers[tracker_id] = tracker

        self._notify_progress_update(tracker, "completed")

    def _check_notification_thresholds(self, tracker_id: str, old_progress: float, new_progress: float):
        """Check and trigger notifications for progress thresholds."""

        notified = self.notified_thresholds[tracker_id]

        for threshold in self.notification_thresholds:
            if old_progress < threshold <= new_progress and threshold not in notified:
                notified.add(threshold)
                tracker = self.trackers[tracker_id]
                self._notify_progress_update(tracker, f"threshold_{threshold}")

    def _update_estimated_completion(self, tracker: ProgressTracker):
        """Update estimated completion time."""

        remaining_time = tracker.estimated_remaining_time
        if remaining_time:
            tracker.estimated_completion = datetime.now() + remaining_time

    def pause_tracking(self, tracker_id: str) -> bool:
        """Pause progress tracking."""

        with self.tracking_lock:
            if tracker_id not in self.trackers:
                return False

            tracker = self.trackers[tracker_id]
            if tracker.status == ProgressStatus.IN_PROGRESS:
                tracker.status = ProgressStatus.PAUSED
                self._notify_progress_update(tracker, "paused")
                return True

        return False

    def resume_tracking(self, tracker_id: str) -> bool:
        """Resume progress tracking."""

        with self.tracking_lock:
            if tracker_id not in self.trackers:
                return False

            tracker = self.trackers[tracker_id]
            if tracker.status == ProgressStatus.PAUSED:
                tracker.status = ProgressStatus.IN_PROGRESS
                self._notify_progress_update(tracker, "resumed")
                return True

        return False

    def cancel_tracking(self, tracker_id: str) -> bool:
        """Cancel progress tracking."""

        with self.tracking_lock:
            if tracker_id not in self.trackers:
                return False

            tracker = self.trackers[tracker_id]
            tracker.status = ProgressStatus.CANCELLED
            tracker.completed_at = datetime.now()

            # Move from active to completed
            if tracker_id in self.active_trackers:
                del self.active_trackers[tracker_id]
            self.completed_trackers[tracker_id] = tracker

            self._notify_progress_update(tracker, "cancelled")
            return True

    def register_callback(self, callback: Callable[[ProgressTracker, str], None]):
        """Register a callback for progress updates."""

        with self.tracking_lock:
            self.update_callbacks.append(callback)

    def _notify_progress_update(self, tracker: ProgressTracker, event_type: str):
        """Notify all registered callbacks of progress updates."""

        for callback in self.update_callbacks:
            try:
                callback(tracker, event_type)
            except Exception as e:
                print(f"Error in progress callback: {e}")

    def get_tracker_status(self, tracker_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed status of a tracker."""

        with self.tracking_lock:
            if tracker_id not in self.trackers:
                return None

            tracker = self.trackers[tracker_id]
            return {
                'id': tracker.id,
                'name': tracker.name,
                'status': tracker.status.value,
                'progress_percentage': tracker.progress_percentage,
                'completed_work': tracker.completed_work,
                'total_work': tracker.total_work,
                'elapsed_time': tracker.elapsed_time.total_seconds() if tracker.elapsed_time else None,
                'estimated_remaining_time': tracker.estimated_remaining_time.total_seconds() if tracker.estimated_remaining_time else None,
                'estimated_completion': tracker.estimated_completion.isoformat() if tracker.estimated_completion else None,
                'checkpoints': [
                    {
                        'name': cp.name,
                        'description': cp.description,
                        'current_value': cp.current_value,
                        'target_value': cp.target_value,
                        'unit': cp.unit,
                        'completed': cp.completed_at is not None,
                        'completed_at': cp.completed_at.isoformat() if cp.completed_at else None
                    }
                    for cp in tracker.checkpoints
                ],
                'metadata': tracker.metadata
            }

    def get_active_trackers(self) -> List[Dict[str, Any]]:
        """Get all active trackers."""

        with self.tracking_lock:
            return [
                {
                    'id': tracker.id,
                    'name': tracker.name,
                    'progress_percentage': tracker.progress_percentage,
                    'status': tracker.status.value,
                    'elapsed_time': tracker.elapsed_time.total_seconds() if tracker.elapsed_time else None,
                    'estimated_completion': tracker.estimated_completion.isoformat() if tracker.estimated_completion else None
                }
                for tracker in self.active_trackers.values()
            ]

    def get_overview_statistics(self) -> Dict[str, Any]:
        """Get overview statistics of all trackers."""

        with self.tracking_lock:
            total_trackers = len(self.trackers)
            active_count = len(self.active_trackers)
            completed_count = len(self.completed_trackers)

            # Calculate average progress of active trackers
            active_progress_values = [t.progress_percentage for t in self.active_trackers.values()]
            avg_active_progress = sum(active_progress_values) / len(active_progress_values) if active_progress_values else 0

            # Find longest running tracker
            longest_running = None
            max_elapsed = timedelta(0)

            for tracker in self.trackers.values():
                if tracker.elapsed_time and tracker.elapsed_time > max_elapsed:
                    max_elapsed = tracker.elapsed_time
                    longest_running = tracker

            return {
                'total_trackers': total_trackers,
                'active_trackers': active_count,
                'completed_trackers': completed_count,
                'cancelled_trackers': sum(1 for t in self.trackers.values() if t.status == ProgressStatus.CANCELLED),
                'average_active_progress': avg_active_progress,
                'longest_running_tracker': {
                    'name': longest_running.name if longest_running else None,
                    'elapsed_time': longest_running.elapsed_time.total_seconds() if longest_running and longest_running.elapsed_time else None
                } if longest_running else None
            }

    def create_hierarchical_tracker(self, parent_name: str, total_work: float,
                                   subtask_configs: List[Dict[str, Any]]) -> str:
        """Create a hierarchical tracker with subtasks."""

        # Create parent tracker
        parent_id = self.create_tracker(parent_name, total_work, ProgressType.TASK)

        # Create subtask trackers
        subtask_ids = []
        for config in subtask_configs:
            subtask_id = self.create_tracker(
                name=config['name'],
                total_work=config['work'],
                progress_type=ProgressType.SUBTASK,
                parent_task=parent_id,
                metadata=config.get('metadata')
            )
            subtask_ids.append(subtask_id)

        # Link subtasks to parent
        with self.tracking_lock:
            if parent_id in self.trackers:
                self.trackers[parent_id].subtasks = subtask_ids

        return parent_id

    def update_hierarchical_progress(self, parent_id: str) -> float:
        """Update parent tracker progress based on subtask completion."""

        with self.tracking_lock:
            if parent_id not in self.trackers:
                return 0.0

            parent_tracker = self.trackers[parent_id]
            total_subtask_work = 0.0
            completed_subtask_work = 0.0

            for subtask_id in parent_tracker.subtasks:
                if subtask_id in self.trackers:
                    subtask = self.trackers[subtask_id]
                    total_subtask_work += subtask.total_work
                    completed_subtask_work += subtask.completed_work

            # Update parent progress proportionally
            if total_subtask_work > 0:
                parent_progress = (completed_subtask_work / total_subtask_work) * parent_tracker.total_work
                parent_tracker.completed_work = parent_progress

                # Check if parent should be marked as completed
                if parent_tracker.progress_percentage >= 100.0:
                    self._mark_completed(parent_id)

                self._notify_progress_update(parent_tracker, "subtask_updated")

            return parent_tracker.progress_percentage

def demo_progress_tracking():
    """Demonstrate the progress tracking system."""
    tracking_system = ProgressTrackingSystem()

    # Create a sample callback
    def progress_callback(tracker: ProgressTracker, event_type: str):
        print(f"Progress Update - {tracker.name}: {event_type} ({tracker.progress_percentage:.1f}%)")

    tracking_system.register_callback(progress_callback)

    print("Progress Tracking Demo")
    print("=" * 50)

    # Create hierarchical tracker
    subtask_configs = [
        {'name': 'Download Files', 'work': 30, 'metadata': {'type': 'download'}},
        {'name': 'Install Components', 'work': 50, 'metadata': {'type': 'installation'}},
        {'name': 'Configure Settings', 'work': 20, 'metadata': {'type': 'configuration'}}
    ]

    parent_id = tracking_system.create_hierarchical_tracker(
        "Install Advanced Analytics Skill",
        total_work=100,
        subtask_configs=subtask_configs
    )

    # Start tracking
    tracking_system.start_tracking(parent_id)

    # Start subtasks
    subtask_ids = tracking_system.trackers[parent_id].subtasks
    for subtask_id in subtask_ids:
        tracking_system.start_tracking(subtask_id)

    # Simulate progress updates
    print("\nSimulating progress updates...")

    # Update subtask progress
    tracking_system.update_progress(subtask_ids[0], 15)  # Download 50%
    tracking_system.update_hierarchical_progress(parent_id)

    tracking_system.update_progress(subtask_ids[0], 30)  # Download 100%
    tracking_system.update_progress(subtask_ids[1], 25)  # Install 50%
    tracking_system.update_hierarchical_progress(parent_id)

    tracking_system.update_progress(subtask_ids[1], 50)  # Install 100%
    tracking_system.update_progress(subtask_ids[2], 20)  # Configure 100%
    tracking_system.update_hierarchical_progress(parent_id)

    # Show final status
    print("\nFinal Status:")
    parent_status = tracking_system.get_tracker_status(parent_id)
    print(f"Parent Task: {parent_status['progress_percentage']:.1f}% - {parent_status['status']}")

    # Show statistics
    stats = tracking_system.get_overview_statistics()
    print(f"\nStatistics:")
    print(f"Total Trackers: {stats['total_trackers']}")
    print(f"Active Trackers: {stats['active_trackers']}")
    print(f"Completed Trackers: {stats['completed_trackers']}")
    print(f"Average Active Progress: {stats['average_active_progress']:.1f}%")

if __name__ == "__main__":
    demo_progress_tracking()
