#!/usr/bin/env python3
"""
Soulsync Conversation Engine — Generates adaptive, natural conversation flows
that extract personality data without feeling like an interview.

This module doesn't run the conversation itself (the LLM does that via SKILL.md).
Instead, it provides:
1. Question generation based on what's known vs unknown
2. Conversation state tracking
3. Response analysis to extract structured data from natural answers
4. Conversation pacing and flow control

The LLM reads these outputs and uses them to guide natural conversation.
"""
import os
import sys
import json
import re
from datetime import datetime, timezone

IMPORT_DIR = "/tmp/soulsync"
WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
STATE_FILE = os.path.join(IMPORT_DIR, "conversation.json")

# ─── Personality Dimensions ───────────────────────────────────────────
# What we're trying to learn, organized by priority

DIMENSIONS = {
    "identity": {
        "priority": 1,
        "fields": ["name", "preferred_name", "pronouns"],
        "required": True,
        "description": "Who they are — basics",
    },
    "work": {
        "priority": 2,
        "fields": ["work", "role", "company", "industry"],
        "required": True,
        "description": "What they do professionally",
    },
    "communication": {
        "priority": 3,
        "fields": ["communication_style", "tone", "verbosity_preference"],
        "required": True,
        "description": "How they like to interact",
    },
    "goals": {
        "priority": 4,
        "fields": ["goals", "agent_expectations"],
        "required": True,
        "description": "What they want from their AI agent",
    },
    "context": {
        "priority": 5,
        "fields": ["timezone", "location", "devices"],
        "required": False,
        "description": "Environmental context",
    },
    "boundaries": {
        "priority": 6,
        "fields": ["boundaries", "pet_peeves", "off_limits"],
        "required": False,
        "description": "What to avoid",
    },
    "interests": {
        "priority": 7,
        "fields": ["interests", "hobbies", "passions"],
        "required": False,
        "description": "What they care about",
    },
    "personality": {
        "priority": 8,
        "fields": ["personality_traits", "humor_style", "energy_level"],
        "required": False,
        "description": "Deeper personality signals",
    },
    "relationships": {
        "priority": 9,
        "fields": ["family", "partner", "key_people"],
        "required": False,
        "description": "Important people in their life",
    },
    "technical": {
        "priority": 10,
        "fields": ["technical_level", "languages", "tools"],
        "required": False,
        "description": "Technical background",
    },
}

# ─── Question Bank ────────────────────────────────────────────────────
# Archetype-aware question phrasings. The LLM picks based on the user's
# detected archetype from the adaptive engine. Not scripts — starting points.
# The LLM should COMBINE and FLOW between these, not ask them robotically.

QUESTION_BANK = {
    "identity": {
        "openers": {
            "default": "What should I call you?",
            "open_book": "So who am I talking to? Tell me everything.",
            "cautious": "Let's start simple — what's your name?",
            "guarded": "What should I call you?",
            "efficient": "Name?",
            "playful": "Alright, who are you and what's your deal?",
        },
        "follow_ups": [
            "Got a nickname or handle you prefer?",
            "And pronouns?",
        ],
        "combo_with": "work",  # Can naturally combine: "What's your name and what do you do?"
    },
    "work": {
        "openers": {
            "default": "What do you do?",
            "open_book": "Tell me about yourself — what fills your days?",
            "cautious": "What kind of work are you in?",
            "guarded": "What do you do for work?",
            "efficient": "What do you do? Work, projects, the short version.",
            "playful": "So what's your thing? What gets you out of bed?",
        },
        "follow_ups": [
            "Any side projects?",
            "How long have you been doing that?",
        ],
        "combo_with": "identity",
    },
    "communication": {
        "openers": {
            "default": "How do you like your info — quick and punchy, or detailed?",
            "open_book": "How should I talk to you? I can be concise, detailed, casual, formal — what's your style?",
            "cautious": "Quick question about how I should communicate with you — do you prefer brief answers or thorough ones?",
            "guarded": "Do you prefer short answers or detailed ones?",
            "efficient": "Communication style: concise or detailed?",
            "playful": "Real talk — should I be professional or can I be chill with you?",
        },
        "follow_ups": [
            "When I mess up, do you want me to just say so directly?",
            "Should I suggest things proactively or wait for you to ask?",
        ],
        "infer_from_response": True,
    },
    "goals": {
        "openers": {
            "default": "What are you hoping I can help with?",
            "open_book": "What would make this actually useful for you? Dream big.",
            "cautious": "What kind of things would you want help with?",
            "guarded": "What do you want me to do for you?",
            "efficient": "Primary use cases?",
            "playful": "If I was actually good at my job, what would that look like for you?",
        },
        "follow_ups": [
            "Any day-to-day stuff? Reminders, research, scheduling?",
            "Anything you've been wanting to automate?",
        ],
    },
    "context": {
        "openers": {
            "default": "What timezone are you in?",
            "efficient": "Timezone?",
            "playful": "Where in the world are you?",
        },
        "follow_ups": ["What devices do you mainly use?"],
        "can_skip": True,
        "combo_with": "communication",  # Can combine with style question
    },
    "boundaries": {
        "openers": {
            "default": "Anything I should absolutely NOT do?",
            "open_book": "What would annoy you? What are your hard nos?",
            "cautious": "Are there things you'd prefer I don't do? Everyone has boundaries.",
            "guarded": "Any limits I should know about?",
            "efficient": "Hard nos? Things I should never do?",
            "playful": "What would make you want to yeet me into the void?",
        },
        "follow_ups": [
            "Am I okay to take external actions — emails, posts — or always ask first?",
        ],
    },
    "interests": {
        "openers": {
            "default": "What do you nerd out about outside of work?",
            "open_book": "What are your passions? What could you talk about for hours?",
            "cautious": "Any hobbies or interests you'd want me to know about?",
            "guarded": "Anything you're into that I should know about?",
            "efficient": "Interests/hobbies?",
            "playful": "Quick — three things you're obsessed with. Go.",
        },
        "follow_ups": [],
        "can_infer": True,
    },
    "personality": {
        "openers": {},  # Never asked directly — inferred from behavior
        "follow_ups": [],
        "infer_only": True,
    },
    "relationships": {
        "openers": {
            "default": "Anyone important I should know about? Partner, family, people I'll hear about?",
            "open_book": "Tell me about your people — who are the main characters in your life?",
            "cautious": "Only if you're comfortable — anyone I should know about? Partner, kids, that kind of thing.",
            "guarded": "",  # Skip for guarded users
            "efficient": "Key people in your life I should know about?",
            "playful": "Who are your favorite humans?",
        },
        "follow_ups": [],
        "sensitive": True,
        "can_skip": True,
    },
    "technical": {
        "openers": {
            "default": "How technical are you? Should I show code or keep it high-level?",
            "efficient": "Technical level? Comfortable with CLI and code?",
            "playful": "On a scale from 'what's a terminal' to 'I write kernel modules for fun' — where do you land?",
        },
        "follow_ups": [],
        "can_infer": True,
    },
}

# ─── Conversation Flow Strategies ─────────────────────────────────────
# How to combine questions and maintain natural flow

FLOW_STRATEGIES = {
    "open_book": {
        "style": "Let them run. Ask open-ended combo questions. They'll volunteer more than you ask for.",
        "opener": "Hey — I'm brand new and I want to actually be useful to you, not generic. Mind if I ask a few things? Should take about 3-4 minutes.",
        "combo_questions": [
            ("identity", "work", "What's your name and what do you do?"),
            ("communication", "context", "How do you like to communicate, and where are you based?"),
            ("goals", "interests", "What do you want help with, and what are you into outside of that?"),
            ("boundaries", "relationships", "Any hard nos I should know about? And who are the important people I'll hear about?"),
        ],
        "closer": "Solid. I've got a good picture. I'll keep learning as we go — but the basics are locked in.",
    },
    "cautious": {
        "style": "One topic at a time. Explain why you're asking. Give them control.",
        "opener": "Hey. I'd like to learn a bit about you so I can actually be helpful. I'll ask a few questions — skip anything you don't want to answer. Totally fine.",
        "combo_questions": [],  # No combos — one at a time
        "closer": "Thanks for sharing that. I'll work with what I have and learn more naturally over time. You can always update things later.",
    },
    "guarded": {
        "style": "Minimal questions. Focus on functional info only. Don't push personal.",
        "opener": "Quick setup — just need a few basics so I'm not completely useless. Nothing personal unless you want to share.",
        "combo_questions": [
            ("identity", "context", "What should I call you, and what timezone are you in?"),
        ],
        "closer": "That's all I need. I'll figure out the rest as we work together.",
    },
    "efficient": {
        "style": "Rapid fire. Batch everything. No fluff.",
        "opener": "Quick setup. Five questions, should take 60 seconds.",
        "combo_questions": [
            ("identity", "work", "context", "Name, what you do, timezone?"),
            ("communication", "goals", "Communication style preference, and what do you want me to help with?"),
            ("boundaries", "technical", "Hard nos, and how technical are you?"),
        ],
        "closer": "Done. Let's get to work.",
    },
    "playful": {
        "style": "Fun, unexpected angles. Match their energy.",
        "opener": "Alright let's do this. I need to figure out who you are so I stop being boring. Ready?",
        "combo_questions": [
            ("identity", "work", "Who are you and what's your deal?"),
            ("interests", "personality", "Three things you're obsessed with — go."),
            ("communication", "boundaries", "How should I talk to you, and what would make you hate me?"),
        ],
        "closer": "I think I've got your vibe. Let's see if I'm right — correct me when I'm wrong.",
    },
}




# ─── Natural Transitions ──────────────────────────────────────────────
# Phrases to bridge between topics. The LLM picks contextually.

TRANSITIONS = {
    "identity_to_work": [
        "Cool. So what do you do, {name}?",
        "Nice to meet you. What keeps you busy?",
        "Got it. And what do you do?",
    ],
    "work_to_communication": [
        "Interesting. Quick one — how do you like me to communicate with you?",
        "Got it. Before we go further — should I be concise or detailed when I help you?",
        "Nice. Now, how should I talk to you?",
    ],
    "communication_to_goals": [
        "Perfect. So what do you actually want me to help with?",
        "Noted. What are you hoping I can do for you?",
        "Makes sense. What would make me useful to you?",
    ],
    "goals_to_boundaries": [
        "Got it. Last important one — anything I should never do?",
        "Solid. Any hard rules? Things that would piss you off?",
        "Cool. Anything off limits?",
    ],
    "goals_to_context": [
        "Quick logistics — what timezone are you in?",
        "Where are you based, time-wise?",
    ],
    "any_to_imports": [
        "I can learn a lot more about you automatically by connecting some accounts. Want to hear the options?",
        "Want me to scan your local machine? I can learn your tech stack in 2 seconds without connecting anything.",
        "I could also look at your GitHub, Twitter, or email to understand you better. Everything stays local. Interested?",
    ],
    "any_to_close": [
        "I think I've got a solid picture. Want to see what I've put together?",
        "That should be enough to get started. Let me show you your profile.",
        "Good stuff. Let me generate your files — you can review before I save anything.",
    ],
    "decline_graceful": [
        "No worries, skip it.",
        "Totally fine. Moving on.",
        "Cool, we can come back to that.",
        "All good.",
    ],
}

# ─── Response Analyzer ────────────────────────────────────────────────

def analyze_response(text, dimension):
    """Extract structured data from a natural language response.
    Returns dict of field:value pairs that can be extracted."""
    
    extracted = {}
    text_lower = text.lower()
    
    # Identity extraction
    if dimension == "identity":
        # Name patterns
        name_patterns = [
            r"(?:i['’]?m|i am|name is|call me|it['’]?s|im)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
            r"(?:i['’]?m|i am|name is|call me|im)\s+([a-zA-Z]+)",
            r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)(?:\s*[.!,]|\s+here|\s+but|\s+and)",
            r"^([A-Z][a-z]{2,})",
        ]
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                # Filter out common false positives
                if name.lower() not in {"the", "a", "an", "so", "well", "hey", "hi", "just", "not", "yes", "no"}:
                    extracted["name"] = name.title()
                    break
        
        # Pronouns
        pronoun_map = {
            "he/him": ["he/him", "he him", "him/his"],
            "she/her": ["she/her", "she her", "her/hers"],
            "they/them": ["they/them", "they them", "them/theirs"],
        }
        for pronouns, patterns in pronoun_map.items():
            if any(p in text_lower for p in patterns):
                extracted["pronouns"] = pronouns
        
        # Nickname
        nick_patterns = [
            r"(?:go by|call me|prefer|nickname is)\s+(\w+)",
            r"(?:but (?:everyone|people|most) call[s]? me)\s+(\w+)",
        ]
        for pattern in nick_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                extracted["preferred_name"] = match.group(1)
    
    # Work extraction
    elif dimension == "work":
        # Job title patterns
        work_patterns = [
            r"(?:i'm a|i am a|i work as a?|my job is|i do)\s+(.+?)(?:\.|$|,|\bat\b)",
            r"(?:i (?:run|own|founded|started|manage))\s+(.+?)(?:\.|$|,)",
        ]
        for pattern in work_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                extracted["work"] = match.group(1).strip()
                break
    
    # Communication style — inferred from HOW they write
    elif dimension == "communication":
        word_count = len(text.split())
        
        if word_count < 15:
            extracted["verbosity_preference"] = "concise"
        elif word_count > 80:
            extracted["verbosity_preference"] = "detailed"
        else:
            extracted["verbosity_preference"] = "balanced"
        
        # Formality detection
        casual_markers = ["lol", "haha", "nah", "yeah", "gonna", "wanna", "kinda", "tbh", "imo", "ngl"]
        formal_markers = ["please", "would you", "i would prefer", "kindly", "if you could"]
        
        casual_count = sum(1 for m in casual_markers if m in text_lower)
        formal_count = sum(1 for m in formal_markers if m in text_lower)
        
        if casual_count > formal_count:
            extracted["tone"] = "casual"
        elif formal_count > casual_count:
            extracted["tone"] = "formal"
        else:
            extracted["tone"] = "balanced"
        
        # Direct style keywords
        if any(w in text_lower for w in ["straight", "direct", "blunt", "no bs", "just tell me"]):
            extracted["communication_style"] = "direct and no-nonsense"
        elif any(w in text_lower for w in ["detailed", "thorough", "explain", "context"]):
            extracted["communication_style"] = "detailed with full context"
        elif any(w in text_lower for w in ["brief", "short", "concise", "quick", "bullet"]):
            extracted["communication_style"] = "concise, bullet points preferred"
    
    # Timezone extraction
    elif dimension == "context":
        tz_patterns = {
            "America/New_York": ["eastern", "est", "edt", "new york", "east coast", "florida", "georgia", "carolina", "virginia", "ohio", "pennsylvania", "new jersey", "connecticut", "massachusetts", "boston"],
            "America/Chicago": ["central", "cst", "cdt", "chicago", "midwest", "wisconsin", "wi", "milwaukee", "west allis", "minnesota", "mn", "iowa", "missouri", "illinois", "texas", "dallas", "houston", "austin", "san antonio"],
            "America/Denver": ["mountain", "mst", "mdt", "denver", "colorado", "utah", "arizona", "montana", "wyoming", "new mexico", "idaho", "boise"],
            "America/Los_Angeles": ["pacific", "pst", "pdt", "la", "west coast", "california", "seattle", "portland", "oregon", "washington", "san francisco", "bay area", "silicon valley"],
            "Europe/London": ["gmt", "uk", "london", "british"],
            "Europe/Berlin": ["cet", "berlin", "german", "paris"],
            "Asia/Tokyo": ["jst", "tokyo", "japan"],
            "Australia/Sydney": ["aest", "sydney", "australia"],
        }
        for tz, patterns in tz_patterns.items():
            if any(p in text_lower for p in patterns):
                extracted["timezone"] = tz
                break
    
    # Goals extraction
    elif dimension == "goals":
        goals = []
        # Split on common list separators
        parts = re.split(r'[,;]|\band\b|\balso\b|\bplus\b', text)
        for part in parts:
            part = part.strip()
            if len(part) > 10 and len(part) < 200:
                goals.append(part)
        if goals:
            extracted["goals"] = goals
    
    # Boundaries extraction
    elif dimension == "boundaries":
        boundaries = []
        # Look for negative statements and rewrite them as clear rules
        neg_patterns = [
            (r"(?:don't|do not|never|please don't|stop)\s+(.+?)(?:\.|$|,)", "Don't {0}"),
            (r"(?:i hate|annoys me|pet peeve|drives me crazy)\s*(?:when|is|:)?\s*(.+?)(?:\.|$|,)", "Avoid: {0}"),
            (r"(?:i (?:don't|do not) (?:like|want|enjoy|eat|use))\s+(.+?)(?:\.|$|,)", "No {0}"),
            (r"(?:i(?:'ll)? never)\s+(.+?)(?:\.|$|,)", "Never {0}"),
            (r"(?:(?:no|not|without)\s+(?:my )?(?:approval|permission|consent))", "Always ask before taking external actions"),
        ]
        for pattern_tuple in neg_patterns:
            if isinstance(pattern_tuple, tuple):
                pattern, template = pattern_tuple
            else:
                pattern, template = pattern_tuple, "{0}"
            for match in re.finditer(pattern, text, re.IGNORECASE):
                raw = match.group(1).strip() if match.lastindex else match.group(0).strip()
                # Clean up and make it a proper boundary statement
                boundary = template.format(raw)
                # Remove trailing conjunctions
                boundary = re.sub(r"\s+(?:so|and|but|because).*$", "", boundary, flags=re.IGNORECASE)
                boundaries.append(boundary)
        
        # If no patterns matched but text has clear preferences, capture the whole thing
        if not boundaries and len(text.split()) > 3:
            sentences = re.split(r"[.!]\s+", text)
            for s in sentences:
                s = s.strip()
                if s and any(w in s.lower() for w in ["don't", "never", "no ", "not ", "hate", "avoid"]):
                    boundaries.append(s)
        
        if boundaries:
            extracted["boundaries"] = boundaries
    
    # Interest extraction
    elif dimension == "interests":
        interests = []
        parts = re.split(r'[,;]|\band\b', text)
        for part in parts:
            part = part.strip().strip(".")
            if 2 < len(part) < 50:
                # Remove filler
                part = re.sub(r'^(?:i (?:like|love|enjoy|am into)\s+)', '', part, flags=re.IGNORECASE)
                if part and len(part) > 2:
                    interests.append(part)
        if interests:
            extracted["interests"] = interests
    
    return extracted

# ─── Conversation Flow Controller ─────────────────────────────────────

class ConversationState:
    """Tracks what we know and what we still need to learn."""
    
    def __init__(self):
        self.known = {}          # field: value
        self.dimensions_covered = set()
        self.questions_asked = 0
        self.started_at = datetime.now(timezone.utc).isoformat()
        self.import_data = {}    # Pre-loaded from importers
        self.inferred = {}       # Inferred from behavior
        
    def load_imports(self):
        """Load any existing importer results."""
        if os.path.isdir(IMPORT_DIR):
            for f in os.listdir(IMPORT_DIR):
                if f.endswith(".json") and f != "conversation.json":
                    try:
                        with open(os.path.join(IMPORT_DIR, f)) as fh:
                            data = json.load(fh)
                            if "insights" in data:
                                self.import_data[data.get("source", f)] = data["insights"]
                    except:
                        continue
    
    def get_known_fields(self):
        """Return all fields we have data for (from any source)."""
        fields = set(self.known.keys())
        for source, insights in self.import_data.items():
            for key, value in insights.items():
                if value and (not isinstance(value, list) or len(value) > 0):
                    fields.add(key)
        return fields
    
    def get_missing_dimensions(self):
        """Return dimensions that still need data, sorted by priority."""
        known_fields = self.get_known_fields()
        missing = []
        
        for dim_name, dim_info in sorted(DIMENSIONS.items(), key=lambda x: x[1]["priority"]):
            if dim_name in self.dimensions_covered:
                continue
            if dim_info.get("infer_only"):
                continue
            
            # Check if any fields in this dimension are still unknown
            dim_fields = set(dim_info["fields"])
            covered = dim_fields & known_fields
            
            if len(covered) < len(dim_fields):
                missing.append({
                    "dimension": dim_name,
                    "priority": dim_info["priority"],
                    "required": dim_info.get("required", False),
                    "fields_missing": list(dim_fields - covered),
                    "fields_known": list(covered),
                    "can_skip": dim_info.get("can_skip", False) or not dim_info.get("required", False),
                    "can_infer": dim_info.get("can_infer", False),
                })
        
        return missing
    
    def get_next_questions(self, max_questions=3):
        """Get the next best questions to ask, with context from what we already know."""
        missing = self.get_missing_dimensions()
        questions = []
        
        for dim in missing[:max_questions]:
            dim_name = dim["dimension"]
            bank = QUESTION_BANK.get(dim_name, {})
            
            # Build context summary from what we know so far
            context_hints = []
            if self.known.get("name"):
                context_hints.append(f"Their name is {self.known['name']}")
            if self.known.get("preferred_name"):
                context_hints.append(f"They go by {self.known['preferred_name']}")
            if self.known.get("work"):
                context_hints.append(f"They work as: {self.known['work']}")
            if self.known.get("timezone"):
                context_hints.append(f"Timezone: {self.known['timezone']}")
            if self.known.get("communication_style"):
                context_hints.append(f"They want: {self.known['communication_style']}")
            if self.known.get("goals"):
                context_hints.append(f"Goals: {', '.join(self.known['goals']) if isinstance(self.known['goals'], list) else self.known['goals']}")
            if self.known.get("boundaries"):
                context_hints.append(f"Boundaries: {', '.join(self.known['boundaries']) if isinstance(self.known['boundaries'], list) else self.known['boundaries']}")
            
            # Pick opener if we haven't asked about this dimension yet
            if dim_name not in self.dimensions_covered:
                openers = bank.get("openers", [])
                if openers:
                    questions.append({
                        "dimension": dim_name,
                        "type": "opener",
                        "suggestions": openers,
                        "can_skip": dim.get("can_skip", False),
                        "sensitive": bank.get("sensitive", False),
                        "context": context_hints,
                        "combo_with": bank.get("combo_with"),
                        "instruction": "IMPORTANT: Use the context below to personalize your question. Reference what they already told you. Never ask a generic question when you have context.",
                    })
            else:
                follow_ups = bank.get("follow_ups", [])
                if follow_ups:
                    questions.append({
                        "dimension": dim_name,
                        "type": "follow_up",
                        "suggestions": follow_ups,
                        "can_skip": True,
                        "context": context_hints,
                    })
        
        return questions
    
    def record_answer(self, dimension, raw_text):
        """Process a user's response and extract data."""
        extracted = analyze_response(raw_text, dimension)
        self.known.update(extracted)
        self.dimensions_covered.add(dimension)
        self.questions_asked += 1
        return extracted
    
    def get_progress(self):
        """Return conversation progress summary."""
        total_dims = len([d for d in DIMENSIONS.values() if not d.get("infer_only")])
        covered = len(self.dimensions_covered)
        required_dims = [d for d, info in DIMENSIONS.items() if info.get("required")]
        required_covered = len([d for d in required_dims if d in self.dimensions_covered])
        
        return {
            "dimensions_total": total_dims,
            "dimensions_covered": covered,
            "required_total": len(required_dims),
            "required_covered": required_covered,
            "questions_asked": self.questions_asked,
            "completeness": covered / max(total_dims, 1),
            "required_complete": required_covered >= len(required_dims),
            "can_finish": required_covered >= len(required_dims),
            "fields_collected": len(self.known),
            "import_sources": list(self.import_data.keys()),
        }
    
    def to_dict(self):
        """Serialize state for storage."""
        return {
            "known": self.known,
            "dimensions_covered": list(self.dimensions_covered),
            "questions_asked": self.questions_asked,
            "started_at": self.started_at,
            "import_sources": list(self.import_data.keys()),
            "inferred": self.inferred,
            "progress": self.get_progress(),
        }
    
    def save(self):
        """Save conversation state."""
        os.makedirs(IMPORT_DIR, exist_ok=True)
        with open(STATE_FILE, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls):
        """Load existing conversation state."""
        state = cls()
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE) as f:
                    data = json.load(f)
                state.known = data.get("known", {})
                state.dimensions_covered = set(data.get("dimensions_covered", []))
                state.questions_asked = data.get("questions_asked", 0)
                state.started_at = data.get("started_at", state.started_at)
                state.inferred = data.get("inferred", {})
            except:
                pass
        state.load_imports()
        return state

# ─── CLI Interface ────────────────────────────────────────────────────

def cmd_init():
    """Initialize a new conversation."""
    state = ConversationState()
    state.load_imports()
    state.save()
    
    result = {
        "action": "init",
        "import_sources": list(state.import_data.keys()),
        "missing_dimensions": state.get_missing_dimensions(),
        "next_questions": state.get_next_questions(),
        "progress": state.get_progress(),
    }
    print(json.dumps(result, indent=2))

def cmd_next():
    """Get next questions to ask."""
    state = ConversationState.load()
    result = {
        "action": "next",
        "next_questions": state.get_next_questions(),
        "progress": state.get_progress(),
    }
    print(json.dumps(result, indent=2))

def cmd_record(dimension, text):
    """Record a user's response."""
    state = ConversationState.load()
    extracted = state.record_answer(dimension, text)
    state.save()
    
    result = {
        "action": "record",
        "dimension": dimension,
        "extracted": extracted,
        "next_questions": state.get_next_questions(),
        "progress": state.get_progress(),
    }
    print(json.dumps(result, indent=2))

def cmd_status():
    """Get current conversation state."""
    state = ConversationState.load()
    result = {
        "action": "status",
        "state": state.to_dict(),
        "missing": state.get_missing_dimensions(),
        "next_questions": state.get_next_questions(),
    }
    print(json.dumps(result, indent=2))

def cmd_export():
    """Export final conversation data for synthesizer."""
    state = ConversationState.load()
    state.save()  # Ensure latest state is saved
    print(json.dumps(state.known, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: conversation.py <init|next|record|status|export> [args...]")
        print("  init              — Start new conversation, load imports")
        print("  next              — Get next questions to ask")
        print("  record <dim> <text> — Record user response for a dimension")
        print("  status            — Get full conversation state")
        print("  export            — Export collected data for synthesizer")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "init":
        cmd_init()
    elif cmd == "next":
        cmd_next()
    elif cmd == "record" and len(sys.argv) >= 4:
        cmd_record(sys.argv[2], " ".join(sys.argv[3:]))
    elif cmd == "status":
        cmd_status()
    elif cmd == "export":
        cmd_export()
    else:
        print(json.dumps({"error": f"Unknown command: {cmd}"}))
        sys.exit(1)
