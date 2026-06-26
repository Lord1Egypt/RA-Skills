"""
Self-Improving Agent - Session Learning Hook

This hook learns from successful sessions to improve future performance.
"""

import json
from pathlib import Path
from datetime import datetime


class SessionLearningHook:
    """Hook for learning from successful sessions."""
    
    def __init__(self):
        self.workspace = Path(__file__).parent.parent
        self.sessions_log = self.workspace / 'learnings' / 'sessions.json'
        
        # Ensure learnings directory exists
        self.sessions_log.parent.mkdir(parents=True, exist_ok=True)
        
    def onSessionEnd(self, session=None):
        """
        Called when a session ends.
        Learn from the session to improve future performance.
        """
        print("📚 Learning from session...")
        
        session_data = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self._extract_session_id(session),
            'duration': self._extract_duration(session),
            'interactions': self._extract_interactions(session),
            'success_patterns': self._extract_success_patterns(session)
        }
        
        # Log the session
        self._log_session(session_data)
        
        print(f"✅ Saved session learning")
    
    def _extract_session_id(self, session):
        """Extract session ID from session object."""
        if session and hasattr(session, 'id'):
            return session.id
        return 'unknown'
    
    def _extract_duration(self, session):
        """Extract session duration."""
        if session and hasattr(session, 'duration'):
            return session.duration
        return 0
    
    def _extract_interactions(self, session):
        """Extract interaction count from session."""
        if session and hasattr(session, 'interactions'):
            return session.interactions
        return 0
    
    def _extract_success_patterns(self, session):
        """Extract success patterns from session."""
        patterns = []
        
        # Analyze what worked well
        if session:
            # Add pattern analysis logic here
            patterns.append('successful_completion')
        
        return patterns
    
    def _log_session(self, session_data):
        """Log session to file."""
        sessions = self._load_sessions()
        sessions.append(session_data)
        self._save_sessions(sessions)
    
    def _load_sessions(self):
        """Load sessions from file."""
        if self.sessions_log.exists():
            with open(self.sessions_log, 'r') as f:
                return json.load(f)
        return []
    
    def _save_sessions(self, sessions):
        """Save sessions to file."""
        with open(self.sessions_log, 'w') as f:
            json.dump(sessions, f, indent=2)


# Create global instance
session_learning_hook = SessionLearningHook()


# Export functions for hook system
def apply():
    """Apply the hook (initialization)."""
    print("🪝 SessionLearningHook initialized")


def onSessionEnd(session=None):
    """Called when a session ends."""
    session_learning_hook.onSessionEnd(session)
