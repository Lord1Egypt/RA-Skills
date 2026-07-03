"""
Signet Mind - Wellness Module
Provides well-being tools: check-ins, exercises, mood tracking.
"""

import random
from typing import List, Dict, Optional
from datetime import datetime, date


class WellnessTools:
    """Well-being tools for Signet Mind."""
    
    # Grounding exercises
    GROUNDING_EXERCISES = {
        "5-4-3-2-1": {
            "name": "5-4-3-2-1 Grounding",
            "description": "A sensory awareness exercise to bring you back to the present.",
            "steps": [
                "Name 5 things you can see around you",
                "Name 4 things you can physically touch",
                "Name 3 things you can hear",
                "Name 2 things you can smell",
                "Name 1 thing you can taste"
            ],
            "duration": "2-5 minutes"
        },
        "box_breathing": {
            "name": "Box Breathing",
            "description": "A calming breathing technique used by Navy SEALs.",
            "steps": [
                "Breathe in slowly for 4 seconds",
                "Hold your breath for 4 seconds",
                "Breathe out slowly for 4 seconds",
                "Hold for 4 seconds",
                "Repeat 4-6 times"
            ],
            "duration": "2-4 minutes"
        },
        "body_scan": {
            "name": "Body Scan Meditation",
            "description": "Release tension by bringing awareness to each part of your body.",
            "steps": [
                "Close your eyes and take a deep breath",
                "Start at your toes, notice any sensations",
                "Move your attention up to your feet, then legs",
                "Continue to your torso, arms, neck, and head",
                "Notice tension and breathe into those areas",
                "Take a moment to feel your whole body"
            ],
            "duration": "5-10 minutes"
        },
        "tensing": {
            "name": "Progressive Muscle Relaxation",
            "description": "Tense and release muscle groups to reduce physical tension.",
            "steps": [
                "Tense your feet for 5 seconds, then release",
                "Tense your calves, then release",
                "Tense your thighs, then release",
                "Tense your arms, then release",
                "Tense your shoulders, then release",
                "Tense your face, then release",
                "Notice the difference between tension and relaxation"
            ],
            "duration": "5-10 minutes"
        }
    }
    
    # Breathing guides
    BREATHING_GUIDES = {
        "calming": {
            "name": "Calming Breath",
            "pattern": "4-7-8",
            "description": "A technique to reduce anxiety and promote sleep.",
            "steps": [
                "Breathe in through your nose for 4 seconds",
                "Hold for 7 seconds",
                "Exhale through mouth for 8 seconds",
                "Repeat 3-4 times"
            ]
        },
        "energizing": {
            "name": "Energizing Breath",
            "pattern": "2-2",
            "description": "Quick breaths to increase alertness.",
            "steps": [
                "Breathe in for 2 seconds",
                "Breathe out for 2 seconds",
                "Repeat 10-15 times rapidly",
                "Then take one deep breath and hold"
            ]
        },
        "balanced": {
            "name": "Balanced Breath",
            "pattern": "4-4-4-4",
            "description": "Balance your nervous system.",
            "steps": [
                "Breathe in for 4 seconds",
                "Hold for 4 seconds",
                "Breathe out for 4 seconds",
                "Hold for 4 seconds",
                "Repeat 5-10 times"
            ]
        }
    }
    
    # Gratitude prompts
    GRATITUDE_PROMPTS = [
        "What's one thing you're grateful for today?",
        "Who is someone that made a positive difference in your life?",
        "What's something small that brought you joy recently?",
        "What's a skill or ability you're thankful for?",
        "What's something in nature you appreciate?"
    ]
    
    # Check-in prompts
    CHECKIN_PROMPTS = [
        "How are you feeling right now?",
        "What's your mood like at the moment?",
        "How's your day going?",
        "What's been on your mind?",
        "How are you doing emotionally?"
    ]
    
    # Mood descriptors for logging
    MOOD_SCALE = [
        (1, "Very Low"),
        (2, "Low"),
        (3, "Somewhat Low"),
        (4, "Below Average"),
        (5, "Neutral"),
        (6, "Above Average"),
        (7, "Good"),
        (8, "Very Good"),
        (9, "Great"),
        (10, "Excellent")
    ]
    
    def __init__(self):
        self.today_mood_logged = False
    
    def get_grounding_exercise(self, name: Optional[str] = None) -> Dict:
        """Get a grounding exercise by name or random."""
        if name and name in self.GROUNDING_EXERCISES:
            return self.GROUNDING_EXERCISES[name]
        return random.choice(list(self.GROUNDING_EXERCISES.values()))
    
    def get_breathing_guide(self, name: Optional[str] = None) -> Dict:
        """Get a breathing guide by name or random."""
        if name and name in self.BREATHING_GUIDES:
            return self.BREATHING_GUIDES[name]
        return random.choice(list(self.BREATHING_GUIDES.values()))
    
    def get_gratitude_prompt(self) -> str:
        """Get a random gratitude prompt."""
        return random.choice(self.GRATITUDE_PROMPTS)
    
    def get_checkin_prompt(self) -> str:
        """Get a check-in prompt."""
        return random.choice(self.CHECKIN_PROMPTS)
    
    def format_grounding_exercise(self, exercise: Dict) -> str:
        """Format a grounding exercise for display."""
        lines = [
            f"**{exercise['name']}**",
            f"_{exercise['description']}_",
            f"Duration: {exercise['duration']}",
            "",
            "Let's do this together:"
        ]
        for i, step in enumerate(exercise['steps'], 1):
            lines.append(f"{i}. {step}")
        
        lines.append("")
        lines.append("Take your time. There's no rush.")
        
        return "\n".join(lines)
    
    def format_breathing_guide(self, guide: Dict) -> str:
        """Format a breathing guide for display."""
        lines = [
            f"**{guide['name']}** ({guide['pattern']})",
            f"_{guide['description']}_",
            ""
        ]
        for i, step in enumerate(guide['steps'], 1):
            lines.append(f"{i}. {step}")
        
        return "\n".join(lines)
    
    def suggest_coping_strategy(self, mood: str) -> str:
        """Suggest a coping strategy based on current mood."""
        mood_lower = mood.lower()
        
        if any(word in mood_lower for word in ["anxious", "worried", "panic", "nervous"]):
            return self.format_grounding_exercise(self.get_grounding_exercise("box_breathing"))
        
        if any(word in mood_lower for word in ["sad", "down", "depressed", "hopeless"]):
            return """Here are some gentle suggestions:

1. **Move gently** - Even a short walk can help
2. **Reach out** - Text or call someone you trust
3. **Self-compassion** - Talk to yourself as you would a friend
4. **Small pleasure** - Do one thing that usually brings you comfort

Would you like to try any of these, or would you prefer to talk?"""
        
        if any(word in mood_lower for word in ["angry", "frustrated", "annoyed"]):
            return """That anger is valid. Here's how to work with it:

1. **Physical outlet** - Punch a pillow, go for a run
2. **Write it out** - Journal without editing
3. **Box breathing** - Counted breaths to calm the nervous system
4. **Time out** - Step away from the situation

What feels right to you?"""
        
        if any(word in mood_lower for word in ["overwhelmed", "stressed", "burnout"]):
            return """Let's break this down:

**Immediate relief:**
- Take 3 deep breaths
- Splash cold water on your face

**Short-term:**
- What ONE thing can you address right now?
- What can wait?
- Can you delegate or say no?

**Remember:** You don't have to do everything at once. What's the most important thing?"""
        
        return """I'm here. Would you like to:
- Talk about what you're feeling?
- Try a breathing exercise?
- Talk about what's on your mind?
- Or just sit together in quiet?"""
    
    def get_mood_scale(self) -> List[tuple]:
        """Return the mood scale for logging."""
        return self.MOOD_SCALE


def get_wellness_tools() -> WellnessTools:
    """Get a WellnessTools instance."""
    return WellnessTools()
