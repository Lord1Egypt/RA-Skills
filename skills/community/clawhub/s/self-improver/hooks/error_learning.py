"""
Self-Improving Agent - Error Learning Hook

This hook learns from errors and recoveries to improve future performance.
"""

import json
from pathlib import Path
from datetime import datetime


class ErrorLearningHook:
    """Hook for learning from errors and recoveries."""
    
    def __init__(self):
        self.workspace = Path(__file__).parent.parent
        self.errors_log = self.workspace / 'learnings' / 'errors.json'
        self.recoveries_log = self.workspace / 'learnings' / 'recoveries.json'
        
        # Ensure learnings directory exists
        self.errors_log.parent.mkdir(parents=True, exist_ok=True)
        
    def onError(self, error):
        """
        Called when an error occurs.
        Learn from the mistake to avoid it in the future.
        """
        print("📝 Learning from error...")
        
        error_data = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': self._extract_context(error)
        }
        
        # Log the error
        self._log_error(error_data)
        
        # Analyze and extract learning
        learning = self._extract_learning(error_data)
        
        # Save the learning
        self._save_learning(learning)
        
        print(f"✅ Saved error learning: {error_data['error_message']}")
    
    def onRecovery(self):
        """
        Called when recovering from an error.
        Learn what worked to recover successfully.
        """
        print("📝 Learning from recovery...")
        
        recovery_data = {
            'timestamp': datetime.now().isoformat(),
            'recovery_method': self._detect_recovery_method()
        }
        
        # Log the recovery
        self._log_recovery(recovery_data)
        
        print(f"✅ Saved recovery learning")
    
    def _extract_context(self, error):
        """Extract context from error."""
        import traceback
        return {
            'traceback': traceback.format_exc()
        }
    
    def _extract_learning(self, error_data):
        """Extract learning from error."""
        return {
            'type': 'error_avoidance',
            'error_type': error_data['error_type'],
            'error_message': error_data['error_message'],
            'prevention': f"Avoid {error_data['error_message']}",
            'timestamp': error_data['timestamp']
        }
    
    def _save_learning(self, learning):
        """Save a single learning to file."""
        # This method was missing - now added
        learnings = self._load_errors()
        learnings.append(learning)
        self._save_errors(learnings)
    
    def _detect_recovery_method(self):
        """Detect what method was used to recover."""
        # This could be enhanced to analyze the recovery process
        return 'automatic_recovery'
    
    def _log_error(self, error_data):
        """Log error to file."""
        errors = self._load_errors()
        errors.append(error_data)
        self._save_errors(errors)
    
    def _log_recovery(self, recovery_data):
        """Log recovery to file."""
        recoveries = self._load_recoveries()
        recoveries.append(recovery_data)
        self._save_recoveries(recoveries)
    
    def _load_errors(self):
        """Load errors from file."""
        if self.errors_log.exists():
            with open(self.errors_log, 'r') as f:
                return json.load(f)
        return []
    
    def _save_errors(self, errors):
        """Save errors to file."""
        with open(self.errors_log, 'w') as f:
            json.dump(errors, f, indent=2)
    
    def _load_recoveries(self):
        """Load recoveries from file."""
        if self.recoveries_log.exists():
            with open(self.recoveries_log, 'r') as f:
                return json.load(f)
        return []
    
    def _save_recoveries(self, recoveries):
        """Save recoveries to file."""
        with open(self.recoveries_log, 'w') as f:
            json.dump(recoveries, f, indent=2)


# Create global instance
error_learning_hook = ErrorLearningHook()


# Export functions for hook system
def apply():
    """Apply the hook (initialization)."""
    print("🪝 ErrorLearningHook initialized")


def onError(error):
    """Called when an error occurs."""
    error_learning_hook.onError(error)


def onRecovery():
    """Called when recovering from an error."""
    error_learning_hook.onRecovery()
