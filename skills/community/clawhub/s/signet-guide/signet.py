"""
Signet Mind - Signet Integration Module
Connects to Signet AI for personalized mental health support.
"""

import json
import subprocess
from pathlib import Path
from typing import Optional, Dict, List
from config import DATA_DIR


SIGNET_PROFILE_PATH = DATA_DIR / "user_profile.json"
SIGNET_CONTEXT_PATH = DATA_DIR / "injected_context.txt"


class SignetConnection:
    """Handles connection to Signet AI for personalized responses."""
    
    def __init__(self):
        self.signet_available = self._check_signet()
        self.user_profile = self._load_profile()
    
    def _check_signet(self) -> bool:
        """Check if Signet is available on the system."""
        try:
            result = subprocess.run(
                ["signet", "--version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def _load_profile(self) -> Dict:
        """Load user profile from Signet if available."""
        if SIGNET_PROFILE_PATH.exists():
            try:
                return json.loads(SIGNET_PROFILE_PATH.read_text())
            except json.JSONDecodeError:
                pass
        return {}
    
    def inject_context(self, context: str):
        """Inject context into Signet for current session."""
        SIGNET_CONTEXT_PATH.write_text(context)
    
    def get_personalized_response(self, user_message: str, conversation_history: List[Dict]) -> str:
        """
        Generate a personalized response using Signet.
        Falls back to basic response if Signet unavailable.
        """
        if not self.signet_available:
            return self._fallback_response(user_message)
        
        # Build context from conversation history and user profile
        context = self._build_context(user_message, conversation_history)
        
        try:
            # Use signet CLI to generate response
            result = subprocess.run(
                ["signet", "chat", "--context", context, "--prompt", user_message],
                capture_output=True,
                timeout=30,
                text=True
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return self._fallback_response(user_message)
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return self._fallback_response(user_message)
    
    def _build_context(self, user_message: str, history: List[Dict]) -> str:
        """Build context string for Signet."""
        context_parts = [
            "You are Signet Mind, a supportive mental health companion.",
            f"User profile: {json.dumps(self.user_profile)}",
            "",
            "Guidelines:",
            "- Provide support, not therapy",
            "- Be warm and empathetic",
            "- Recognize patterns in user's mood",
            "- Suggest coping strategies when appropriate",
            "- Always prioritize user's safety",
            "",
            "Recent conversation:"
        ]
        
        # Add last 5 conversation turns
        for turn in history[-5:]:
            context_parts.append(f"User: {turn.get('user', '')}")
            context_parts.append(f"You: {turn.get('ai', '')}")
        
        context_parts.append(f"\nCurrent message: {user_message}")
        
        return "\n".join(context_parts)
    
    def _fallback_response(self, user_message: str) -> str:
        """Fallback response when Signet is unavailable."""
        # Basic mental health support responses
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ["suicidal", "want to die", "end it all", "hurt myself"]):
            return self._crisis_response()
        
        if any(word in message_lower for word in ["anxious", "anxiety", "worried", "panic"]):
            return """I hear that you're feeling anxious. Let's try this grounding exercise:

**5-4-3-2-1 Technique:**
- Name 5 things you can see
- 4 things you can touch
- 3 things you can hear
- 2 things you can smell
- 1 thing you can taste

Would you like to try this together, or would you prefer to talk about what's causing the anxiety?"""
        
        if any(word in message_lower for word in ["sad", "depressed", "down", "hopeless"]):
            return """I'm here with you. It sounds like you're going through a difficult time.

Would you like to share what's on your mind? Sometimes talking about it can help, even if it doesn't feel like it right now.

If you'd like, I can also suggest some gentle activities that might help lift your mood a little."""
        
        if any(word in message_lower for word in ["stress", "stressed", "overwhelmed"]):
            return """I can sense you're feeling overwhelmed. Let's take a moment together.

**Box Breathing:** Try this:
- Breathe in for 4 seconds
- Hold for 4 seconds
- Breathe out for 4 seconds
- Hold for 4 seconds
- Repeat 4 times

Would you like to try this, or tell me what's causing the stress?"""
        
        return """I'm here to support you. Tell me more about what you're experiencing. How are you feeling right now?"""
    
    def _crisis_response(self) -> str:
        """Response for crisis situations."""
        return """I'm very concerned about you right now. Please reach out for immediate help:

**Ireland:**
- Samaritans: 116 123
- Pieta House: 1800 247 247
- Emergency: 112

**UK:**
- Samaritans: 116 123
- Mind: 0300 123 3393
- Emergency: 999

If you're in immediate danger, please call emergency services (112 or 999) now.

You don't have to face this alone. Is there someone you can contact right now?"""
    
    def learn_from_interaction(self, user_message: str, ai_response: str, feedback: Optional[str] = None):
        """Learn from this interaction to improve future responses."""
        # In production, this would update the Signet profile
        # For now, we track preferences locally
        if feedback:
            prefs = json.loads(SIGNET_PROFILE_PATH.read_text()) if SIGNET_PROFILE_PATH.exists() else {}
            prefs["last_feedback"] = feedback
            prefs["last_interaction"] = user_message[:100]
            SIGNET_PROFILE_PATH.write_text(json.dumps(prefs, indent=2))


def get_signet_connection() -> SignetConnection:
    """Get a Signet connection instance."""
    return SignetConnection()
