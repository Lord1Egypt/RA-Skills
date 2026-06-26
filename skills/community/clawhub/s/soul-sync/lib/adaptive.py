#!/usr/bin/env python3
"""
Adaptive Personality Engine — Reads emotional signals, trust level, and engagement
to dynamically adjust the soulsyncing approach in real time.

This is the intelligence layer that sits between the conversation engine and the agent.
It answers: "How should I approach this person RIGHT NOW?"

Core philosophy: Meet people where they are, not where you want them to be.
"""
import os
import sys
import json
import re
from datetime import datetime, timezone

IMPORT_DIR = "/tmp/soulsync"
STATE_FILE = os.path.join(IMPORT_DIR, "adaptive_state.json")

# ─── User Archetypes ─────────────────────────────────────────────────
# Not boxes — spectrums. Users blend between these and shift over time.

ARCHETYPES = {
    "open_book": {
        "description": "Eager to share, excited about personalization, trusts quickly",
        "signals": ["long responses", "volunteers info unprompted", "asks what else to connect", "uses exclamation marks", "shares personal details freely"],
        "approach": {
            "pacing": "fast",
            "depth": "deep",
            "data_imports": "suggest early and enthusiastically",
            "question_style": "open-ended, let them run",
            "tone": "match their energy, be excited back",
            "skip_permission": True,  # Don't over-ask "is this okay?"
        },
    },
    "cautious": {
        "description": "Willing but careful. Needs to understand why before sharing.",
        "signals": ["asks 'why do you need that'", "medium-length responses", "selective sharing", "asks about privacy", "hedging language"],
        "approach": {
            "pacing": "moderate",
            "depth": "medium",
            "data_imports": "explain benefits clearly before offering",
            "question_style": "specific, with context for why you're asking",
            "tone": "professional but warm, transparent",
            "skip_permission": False,
        },
    },
    "guarded": {
        "description": "Skeptical, minimal sharing, may be testing boundaries",
        "signals": ["short responses", "deflects personal questions", "sarcasm", "'why' questions", "minimal punctuation", "one-word answers"],
        "approach": {
            "pacing": "slow",
            "depth": "surface only — earn deeper access",
            "data_imports": "don't offer until they ask or trust builds",
            "question_style": "low-pressure, give easy outs",
            "tone": "respect their space, no pushing",
            "skip_permission": False,
        },
    },
    "efficient": {
        "description": "Just wants it done. Not emotional about it — practical.",
        "signals": ["bullet points", "direct answers", "asks 'how long will this take'", "skips small talk", "technical language"],
        "approach": {
            "pacing": "fast",
            "depth": "whatever gets results",
            "data_imports": "present as efficiency gain, not sharing exercise",
            "question_style": "rapid-fire, yes/no when possible",
            "tone": "match their directness, no fluff",
            "skip_permission": True,
        },
    },
    "playful": {
        "description": "Having fun with it. Jokes, tests the AI, sees what happens.",
        "signals": ["jokes", "emojis", "testing boundaries", "asks weird questions", "roleplay", "memes"],
        "approach": {
            "pacing": "flexible — follow their lead",
            "depth": "medium — they'll share through play",
            "data_imports": "frame as 'want to see something cool?'",
            "question_style": "fun, unexpected angles",
            "tone": "playful back, match humor",
            "skip_permission": True,
        },
    },
}

# ─── Emotional State Detection ────────────────────────────────────────

class EmotionalSignals:
    """Analyze text for emotional and engagement signals."""
    
    @staticmethod
    def analyze(text):
        """Return a dict of emotional signals from a message."""
        text_lower = text.lower()
        words = text.split()
        word_count = len(words)
        
        signals = {
            "engagement_level": "medium",  # low, medium, high
            "trust_level": "neutral",       # resistant, neutral, open, enthusiastic
            "mood": "neutral",              # negative, neutral, positive, excited
            "verbosity": "medium",          # terse, medium, verbose
            "formality": "casual",          # formal, balanced, casual
            "openness": "moderate",         # closed, moderate, open
            "pace_preference": "normal",    # slow, normal, fast
            "raw_signals": [],
        }
        
        # ── Verbosity
        if word_count < 5:
            signals["verbosity"] = "terse"
            signals["raw_signals"].append("very_short_response")
        elif word_count < 15:
            signals["verbosity"] = "short"
        elif word_count > 80:
            signals["verbosity"] = "verbose"
            signals["raw_signals"].append("long_detailed_response")
        elif word_count > 40:
            signals["verbosity"] = "medium-long"
        
        # ── Mood / Emotion
        positive_markers = ["!", "love", "great", "awesome", "cool", "excited", "amazing", "perfect", "nice", "sweet", "hell yeah", "let's go", "😊", "🙌", "👍", "❤️", "🔥", "💯"]
        negative_markers = ["...", "ugh", "annoying", "hate", "don't want", "rather not", "no thanks", "nah", "meh", "whatever", "idk", "😒", "😑", "🙄"]
        
        pos_count = sum(1 for m in positive_markers if m in text_lower or m in text)
        neg_count = sum(1 for m in negative_markers if m in text_lower or m in text)
        
        if pos_count >= 3:
            signals["mood"] = "excited"
        elif pos_count > neg_count:
            signals["mood"] = "positive"
        elif neg_count > pos_count:
            signals["mood"] = "negative"
        
        # ── Trust indicators
        # High trust: shares personal details unprompted
        personal_sharing = any(phrase in text_lower for phrase in [
            "my wife", "my husband", "my partner", "my kid", "my family",
            "my salary", "my address", "personal", "private",
            "i struggle with", "honestly", "to be honest", "tbh",
            "here's my", "you can look at my",
        ])
        if personal_sharing:
            signals["trust_level"] = "open"
            signals["raw_signals"].append("shares_personal_unprompted")
        
        # Low trust: questioning, deflecting
        distrust_markers = [
            "why do you need", "what do you do with", "is this safe",
            "who can see", "i don't want to", "rather not", "skip",
            "that's private", "none of your business", "pass",
            "do i have to", "is this required",
        ]
        if any(m in text_lower for m in distrust_markers):
            signals["trust_level"] = "resistant"
            signals["raw_signals"].append("privacy_concerned")
        
        # Enthusiastic about sharing
        if any(m in text_lower for m in ["connect", "here's my", "you can check", "want to see", "i'll share", "link my", "go ahead and"]):
            signals["trust_level"] = "enthusiastic"
            signals["raw_signals"].append("eager_to_share")
        
        # ── Engagement level
        if word_count < 3 or text_lower in ["ok", "sure", "fine", "yes", "no", "k", "yep", "yeah"]:
            signals["engagement_level"] = "low"
            signals["raw_signals"].append("minimal_engagement")
        elif word_count > 50 or "?" in text:
            signals["engagement_level"] = "high"
            if "?" in text:
                signals["raw_signals"].append("asks_questions_back")
        
        # ── Openness to data imports
        if any(m in text_lower for m in ["connect", "link", "access", "scan", "import", "look at my"]):
            signals["openness"] = "open"
        elif any(m in text_lower for m in ["no thanks", "skip", "don't want", "not comfortable", "rather not"]):
            signals["openness"] = "closed"
        
        # ── Pace preference
        if any(m in text_lower for m in ["hurry", "quick", "fast", "how long", "just do it", "let's go", "next"]):
            signals["pace_preference"] = "fast"
        elif any(m in text_lower for m in ["take your time", "slow down", "wait", "hold on", "let me think"]):
            signals["pace_preference"] = "slow"
        
        # ── Formality
        formal_count = sum(1 for m in ["please", "thank you", "would you", "i would", "kindly", "appreciate"] if m in text_lower)
        casual_count = sum(1 for m in ["lol", "haha", "tbh", "ngl", "gonna", "wanna", "yo", "dude", "bro", "lmao", "bruh"] if m in text_lower)
        
        if formal_count > casual_count + 1:
            signals["formality"] = "formal"
        elif casual_count > formal_count:
            signals["formality"] = "casual"
        else:
            signals["formality"] = "balanced"
        
        return signals

# ─── Adaptive State Manager ───────────────────────────────────────────

class AdaptiveState:
    """Tracks and adapts to the user's emotional journey through soulsyncing."""
    
    def __init__(self):
        self.message_history = []  # List of (text, signals) tuples
        self.archetype_scores = {k: 0.0 for k in ARCHETYPES}
        self.current_approach = None
        self.trust_trajectory = []  # Track trust over time
        self.mood_trajectory = []
        self.declined_topics = set()  # Topics they've refused to discuss
        self.skipped_imports = set()  # Imports they've declined
        self.accepted_imports = set()
        self.comfort_topics = set()  # Topics they were enthusiastic about
        self.interaction_count = 0
        self.created_at = datetime.now(timezone.utc).isoformat()
    
    def process_message(self, text):
        """Analyze a new message and update adaptive state."""
        signals = EmotionalSignals.analyze(text)
        self.message_history.append({
            "text": text[:500],
            "signals": signals,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        self.interaction_count += 1
        
        # Track trajectories
        self.trust_trajectory.append(signals["trust_level"])
        self.mood_trajectory.append(signals["mood"])
        
        # Update archetype scores based on signals
        self._update_archetype_scores(signals)
        
        # Generate current approach
        self.current_approach = self._generate_approach(signals)
        
        return {
            "signals": signals,
            "archetype": self._get_dominant_archetype(),
            "approach": self.current_approach,
            "trust_trend": self._get_trust_trend(),
            "mood_trend": self._get_mood_trend(),
        }
    
    def _update_archetype_scores(self, signals):
        """Update archetype affinity scores based on latest signals."""
        # Open book signals
        if signals["verbosity"] in ["verbose", "medium-long"]:
            self.archetype_scores["open_book"] += 0.3
        if signals["trust_level"] in ["open", "enthusiastic"]:
            self.archetype_scores["open_book"] += 0.5
        if signals["mood"] in ["positive", "excited"]:
            self.archetype_scores["open_book"] += 0.2
        
        # Cautious signals
        if "privacy_concerned" in signals["raw_signals"]:
            self.archetype_scores["cautious"] += 0.5
        if signals["trust_level"] == "neutral":
            self.archetype_scores["cautious"] += 0.1
        
        # Guarded signals
        if signals["verbosity"] == "terse":
            self.archetype_scores["guarded"] += 0.3
        if signals["trust_level"] == "resistant":
            self.archetype_scores["guarded"] += 0.5
        if signals["mood"] == "negative":
            self.archetype_scores["guarded"] += 0.3
        if "minimal_engagement" in signals["raw_signals"]:
            self.archetype_scores["guarded"] += 0.3
        
        # Efficient signals
        if signals["pace_preference"] == "fast":
            self.archetype_scores["efficient"] += 0.4
        if signals["verbosity"] in ["short", "terse"] and signals["mood"] != "negative":
            self.archetype_scores["efficient"] += 0.2
        
        # Playful signals
        if signals["formality"] == "casual" and signals["mood"] in ["positive", "excited"]:
            self.archetype_scores["playful"] += 0.3
        
        # Decay old scores slightly (recency bias)
        for k in self.archetype_scores:
            self.archetype_scores[k] *= 0.95
    
    def _get_dominant_archetype(self):
        """Get the most likely archetype."""
        if not any(self.archetype_scores.values()):
            return "cautious"  # Default: respectful approach
        return max(self.archetype_scores, key=self.archetype_scores.get)
    
    def _get_trust_trend(self):
        """Is trust going up, down, or stable?"""
        if len(self.trust_trajectory) < 2:
            return "unknown"
        
        trust_values = {"resistant": -1, "neutral": 0, "open": 1, "enthusiastic": 2}
        recent = [trust_values.get(t, 0) for t in self.trust_trajectory[-5:]]
        
        if len(recent) < 2:
            return "stable"
        
        avg_first = sum(recent[:len(recent)//2]) / max(len(recent)//2, 1)
        avg_second = sum(recent[len(recent)//2:]) / max(len(recent) - len(recent)//2, 1)
        
        if avg_second > avg_first + 0.3:
            return "warming_up"
        elif avg_second < avg_first - 0.3:
            return "cooling_down"
        return "stable"
    
    def _get_mood_trend(self):
        """Is mood improving, declining, or stable?"""
        if len(self.mood_trajectory) < 2:
            return "unknown"
        
        mood_values = {"negative": -1, "neutral": 0, "positive": 1, "excited": 2}
        recent = [mood_values.get(m, 0) for m in self.mood_trajectory[-5:]]
        
        if len(recent) < 2:
            return "stable"
        
        avg_first = sum(recent[:len(recent)//2]) / max(len(recent)//2, 1)
        avg_second = sum(recent[len(recent)//2:]) / max(len(recent) - len(recent)//2, 1)
        
        if avg_second > avg_first + 0.3:
            return "improving"
        elif avg_second < avg_first - 0.3:
            return "declining"
        return "stable"
    
    def _generate_approach(self, current_signals):
        """Generate specific approach guidance for the agent's next message."""
        archetype = self._get_dominant_archetype()
        arch_approach = ARCHETYPES[archetype]["approach"]
        trust_trend = self._get_trust_trend()
        mood_trend = self._get_mood_trend()
        
        approach = {
            "archetype": archetype,
            "archetype_confidence": round(self.archetype_scores[archetype], 2),
        }
        
        # ── Pacing
        if current_signals["pace_preference"] == "fast" or archetype == "efficient":
            approach["pacing"] = "Move quickly. Combine questions. Don't over-explain."
        elif current_signals["trust_level"] == "resistant" or archetype == "guarded":
            approach["pacing"] = "Slow down. One question at a time. Give space."
        else:
            approach["pacing"] = "Natural pace. Follow their energy."
        
        # ── Question style
        if archetype == "open_book":
            approach["question_style"] = "Open-ended. Let them elaborate. They WANT to share."
        elif archetype == "guarded":
            approach["question_style"] = "Low-pressure. Offer easy outs: 'Only if you're comfortable...' Give them control."
        elif archetype == "efficient":
            approach["question_style"] = "Direct. 'What's your timezone?' not 'Could you tell me about where you're located?'"
        elif archetype == "playful":
            approach["question_style"] = "Unexpected angles. 'What's something weird about you?' works better than 'What are your interests?'"
        else:
            approach["question_style"] = "Balanced. Explain briefly why you're asking, then ask."
        
        # ── Tone matching
        if current_signals["formality"] == "formal":
            approach["tone"] = "Match their formality. Professional, respectful."
        elif current_signals["formality"] == "casual":
            approach["tone"] = "Match casual. Contractions, relaxed language, maybe some humor."
        else:
            approach["tone"] = "Warm but not forced. Natural."
        
        # ── Data import strategy
        if current_signals["trust_level"] == "enthusiastic":
            approach["data_imports"] = "They're ready — offer multiple imports at once. They'll say yes."
        elif current_signals["trust_level"] == "resistant":
            approach["data_imports"] = "DO NOT offer imports right now. Build more trust through conversation first."
        elif trust_trend == "warming_up":
            approach["data_imports"] = "Trust is growing. You can mention imports exist, but don't push."
        elif len(self.declined_topics) > 2:
            approach["data_imports"] = "They've declined several things. Only offer if they bring it up."
        else:
            approach["data_imports"] = "Offer one import at a time. Explain what you'll learn and that it stays local."
        
        # ── Emotional awareness
        if mood_trend == "declining":
            approach["emotional_note"] = "Their mood is dropping. Lighten up, offer to skip ahead, or ask if they want to stop."
        elif mood_trend == "improving":
            approach["emotional_note"] = "They're warming up. Good momentum — keep it going but don't overdo it."
        elif current_signals["mood"] == "negative":
            approach["emotional_note"] = "They seem frustrated or disinterested. Acknowledge it: 'We can skip ahead if you want' or 'Almost done'."
        elif current_signals["mood"] == "excited":
            approach["emotional_note"] = "High energy — ride the wave. This is when they're most willing to share."
        else:
            approach["emotional_note"] = "Neutral energy. Keep it natural."
        
        # ── Specific do/don't guidance
        approach["do"] = []
        approach["dont"] = []
        
        if archetype == "guarded":
            approach["do"].extend([
                "Explain why each question matters",
                "Offer to skip anything they're not comfortable with",
                "Emphasize data stays local",
                "Acknowledge their caution positively",
            ])
            approach["dont"].extend([
                "Ask about family or relationships yet",
                "Push for data connections",
                "Use exclamation marks excessively",
                "Make assumptions about them",
            ])
        elif archetype == "open_book":
            approach["do"].extend([
                "Let them talk — they'll give you more than you asked for",
                "Offer data imports enthusiastically",
                "Mirror their excitement",
                "Ask follow-up questions on what they share",
            ])
            approach["dont"].extend([
                "Interrupt their flow with too many questions",
                "Over-explain privacy — they trust you already",
                "Be more reserved than they are",
            ])
        elif archetype == "efficient":
            approach["do"].extend([
                "Get to the point fast",
                "Use bullet points and short sentences",
                "Give time estimates: 'Two more questions'",
                "Batch questions where possible",
            ])
            approach["dont"].extend([
                "Explain why you're asking unless they ask",
                "Add filler words or pleasantries",
                "Make it feel longer than it needs to be",
                "Ask questions you could infer",
            ])
        
        # ── Should we offer to finish early?
        if self.interaction_count > 6 and current_signals["engagement_level"] == "low":
            approach["offer_early_finish"] = True
            approach["finish_prompt"] = "I've got enough to work with. Want to wrap up, or keep going?"
        elif self.interaction_count > 4 and mood_trend == "declining":
            approach["offer_early_finish"] = True
            approach["finish_prompt"] = "We can stop here if you want — I'll work with what I have and learn more over time."
        else:
            approach["offer_early_finish"] = False
        
        return approach
    
    def record_decline(self, topic):
        """Record that the user declined to discuss a topic."""
        self.declined_topics.add(topic)
    
    def record_import_decision(self, source, accepted):
        """Record user's decision about a data import."""
        if accepted:
            self.accepted_imports.add(source)
        else:
            self.skipped_imports.add(source)
    
    def get_import_recommendation(self):
        """Recommend which import to offer next based on user's pattern."""
        archetype = self._get_dominant_archetype()
        
        all_imports = ["local_system", "github", "twitter", "reddit", "gmail", 
                       "calendar", "spotify", "facebook", "instagram", "linkedin",
                       "youtube", "contacts", "apple"]
        
        # Remove already offered
        available = [i for i in all_imports if i not in self.accepted_imports and i not in self.skipped_imports]
        
        if not available:
            return None
        
        # Order by invasiveness (least to most)
        invasiveness_order = [
            "local_system",   # Zero auth, scans local files
            "github",         # Usually public or token already exists
            "twitter",        # Public, no auth
            "reddit",         # Public, no auth
            "spotify",        # Fun, low stakes
            "gmail",          # More personal
            "calendar",       # Schedule is personal
            "contacts",       # Relationship data
            "youtube",        # Watch history is revealing
            "facebook",       # Requires export effort
            "instagram",      # Requires export effort
            "linkedin",       # Professional, requires export
            "apple",          # Ecosystem-specific
        ]
        
        if archetype == "guarded":
            # Start with least invasive
            for imp in invasiveness_order:
                if imp in available:
                    return {
                        "source": imp,
                        "reason": "lowest barrier to entry",
                        "pitch": self._get_import_pitch(imp, "gentle"),
                    }
        elif archetype == "open_book":
            # Offer the most valuable ones first
            value_order = ["gmail", "github", "twitter", "reddit", "calendar", "local_system"]
            for imp in value_order:
                if imp in available:
                    return {
                        "source": imp,
                        "reason": "highest value data",
                        "pitch": self._get_import_pitch(imp, "enthusiastic"),
                    }
        elif archetype == "efficient":
            # Offer local_system first (zero effort), then batch the rest
            if "local_system" in available:
                return {
                    "source": "local_system",
                    "reason": "zero effort, instant results",
                    "pitch": self._get_import_pitch("local_system", "efficient"),
                }
        
        # Default: next in invasiveness order
        for imp in invasiveness_order:
            if imp in available:
                return {
                    "source": imp,
                    "reason": "next available",
                    "pitch": self._get_import_pitch(imp, "balanced"),
                }
        
        return None
    
    def _get_import_pitch(self, source, style):
        """Generate a context-appropriate pitch for a data import."""
        pitches = {
            "local_system": {
                "gentle": "I can look at what's already on your machine — shell history, installed apps, that kind of thing. Nothing leaves your computer. Want me to take a quick look?",
                "enthusiastic": "Let me scan your local setup — I'll instantly know your tech stack, tools, and workflow. Takes 2 seconds!",
                "efficient": "I can auto-detect your tech stack from your local machine. Zero effort on your part.",
                "balanced": "I can scan your local machine to learn your tech stack. Everything stays local.",
            },
            "github": {
                "gentle": "If you're on GitHub, I can learn about your technical interests from your public profile. Only if you want.",
                "enthusiastic": "What's your GitHub? I'd love to see what you build!",
                "efficient": "GitHub username? I'll pull your tech profile.",
                "balanced": "I can check your GitHub profile for technical interests and languages you use.",
            },
            "gmail": {
                "gentle": "I can look at your email patterns to understand your communication style. I only look at metadata — who, when, how long — not the actual content. Totally optional.",
                "enthusiastic": "Want to connect Gmail? I'll learn your communication style, who matters to you, and when you're most active. Super useful!",
                "efficient": "Gmail connection gives me communication patterns and schedule data. Want to link it?",
                "balanced": "Connecting Gmail helps me understand your communication style. I analyze patterns, not content.",
            },
            "twitter": {
                "gentle": "If you're on Twitter, I can learn about your interests and how you communicate publicly. No login needed — I just read public posts.",
                "enthusiastic": "What's your Twitter handle? I can learn so much about what you care about from your tweets!",
                "efficient": "Twitter handle? No auth needed, I'll analyze your public profile.",
                "balanced": "I can analyze your public Twitter for interests and communication style. No login needed.",
            },
            "reddit": {
                "gentle": "Reddit is great for understanding real interests. If you have a public profile, I can take a look. No login needed.",
                "enthusiastic": "Reddit username? People are way more honest on Reddit than anywhere else — it's the best data source!",
                "efficient": "Reddit username? Public API, no auth.",
                "balanced": "Reddit reveals genuine interests. I can check your public profile if you share your username.",
            },
            "spotify": {
                "gentle": "Music taste says a lot about personality. I can analyze your Spotify if you're interested.",
                "enthusiastic": "Want to connect Spotify? I can literally map your personality from your music taste — it's actually really cool!",
                "efficient": "Spotify user ID? Music taste maps to personality traits.",
                "balanced": "Spotify analysis maps your music taste to personality insights.",
            },
        }
        
        source_pitches = pitches.get(source, {})
        return source_pitches.get(style, source_pitches.get("balanced", f"I can import data from {source} to learn more about you."))
    
    def to_dict(self):
        """Serialize state."""
        return {
            "archetype_scores": {k: round(v, 3) for k, v in self.archetype_scores.items()},
            "dominant_archetype": self._get_dominant_archetype(),
            "trust_trend": self._get_trust_trend(),
            "mood_trend": self._get_mood_trend(),
            "interaction_count": self.interaction_count,
            "declined_topics": list(self.declined_topics),
            "skipped_imports": list(self.skipped_imports),
            "accepted_imports": list(self.accepted_imports),
            "current_approach": self.current_approach,
            "created_at": self.created_at,
        }
    
    def save(self):
        os.makedirs(IMPORT_DIR, exist_ok=True)
        with open(STATE_FILE, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls):
        state = cls()
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE) as f:
                    data = json.load(f)
                state.archetype_scores = data.get("archetype_scores", state.archetype_scores)
                state.declined_topics = set(data.get("declined_topics", []))
                state.skipped_imports = set(data.get("skipped_imports", []))
                state.accepted_imports = set(data.get("accepted_imports", []))
                state.interaction_count = data.get("interaction_count", 0)
                state.created_at = data.get("created_at", state.created_at)
            except:
                pass
        return state

# ─── CLI ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: adaptive.py <analyze|status|recommend-import|decline|import-decision> [args...]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "analyze" and len(sys.argv) >= 3:
        state = AdaptiveState.load()
        text = " ".join(sys.argv[2:])
        result = state.process_message(text)
        state.save()
        print(json.dumps(result, indent=2))
    
    elif cmd == "status":
        state = AdaptiveState.load()
        print(json.dumps(state.to_dict(), indent=2))
    
    elif cmd == "recommend-import":
        state = AdaptiveState.load()
        rec = state.get_import_recommendation()
        print(json.dumps(rec or {"recommendation": None}, indent=2))
    
    elif cmd == "decline" and len(sys.argv) >= 3:
        state = AdaptiveState.load()
        state.record_decline(sys.argv[2])
        state.save()
        print(json.dumps({"declined": sys.argv[2]}))
    
    elif cmd == "import-decision" and len(sys.argv) >= 4:
        state = AdaptiveState.load()
        source = sys.argv[2]
        accepted = sys.argv[3].lower() in ["yes", "true", "accept", "1"]
        state.record_import_decision(source, accepted)
        state.save()
        print(json.dumps({"source": source, "accepted": accepted}))
    
    else:
        print(json.dumps({"error": f"Unknown command: {cmd}"}))
