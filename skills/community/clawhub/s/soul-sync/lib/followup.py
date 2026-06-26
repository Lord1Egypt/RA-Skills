#!/usr/bin/env python3
"""
Soulsync Follow-Up Engine — Ongoing personalization after initial setup.

Handles:
1. Periodic check-ins ("It's been 2 weeks, anything changed?")
2. Life event detection ("You mentioned a new job — want to update your profile?")
3. Correction learning (when user says "that's wrong" or "actually I...")
4. Deep dives (unlocking new dimensions over time as trust builds)
5. Data source suggestions ("You've been talking about code a lot — want to connect GitHub?")
"""
import os
import sys
import json
import re
from datetime import datetime, timezone, timedelta

WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
STATE_FILE = os.path.join(WORKSPACE, ".soulsync-state.json")

# ─── Life Change Signals ──────────────────────────────────────────────
# Phrases that suggest something in the user's life changed

LIFE_CHANGE_SIGNALS = {
    "job": [
        "new job", "got hired", "started working at", "quit my job", "got fired",
        "changing careers", "got promoted", "new role", "left my job", "freelancing now",
    ],
    "location": [
        "moving to", "just moved", "relocated", "new house", "new apartment",
        "bought a house", "sold my house",
    ],
    "relationship": [
        "got married", "engaged", "broke up", "divorced", "new partner",
        "having a baby", "pregnant", "new kid",
    ],
    "interests": [
        "really into", "just discovered", "started learning", "obsessed with",
        "picked up", "new hobby", "quit", "stopped doing",
    ],
    "technical": [
        "switched to", "learning", "started using", "dropped", "migrated to",
        "new setup", "new machine", "rebuilt my",
    ],
}

# ─── Correction Patterns ─────────────────────────────────────────────
# When the user corrects something about themselves

CORRECTION_PATTERNS = [
    r"^(?:actually|no|wait|hang on),?",
    r"(?:that's|that is) (?:wrong|incorrect|not right|not true)",
    r"(?:i (?:don't|no longer|stopped|quit)\s+(.+?)(?:\.|$|,))",
    r"(?:i (?:actually|now)\s+(.+?)(?:\.|$|,))",
    r"(?:correct(?:ion)?:?\s+(.+?)(?:\.|$))",
    r"(?:update (?:my|the)\s+(?:profile|soul|user|info))",
]


class FollowUpState:
    """Tracks when and how to follow up with the user."""
    
    def __init__(self):
        self.initial_sync_date = None
        self.last_followup_date = None
        self.followup_count = 0
        self.corrections_made = []
        self.life_changes_detected = []
        self.suggested_imports = []
        self.declined_imports = []
        self.trust_level = "initial"  # initial → comfortable → trusted
        self.dimensions_unlocked = []  # dimensions revealed over time
        self.ongoing_enabled = None    # None = not asked yet, True/False = user chose
        self.passive_learning = True   # Always-on light learning from normal chat
        self.pending_confirmations = [] # Facts to confirm casually
        self.learned_passively = []    # Things picked up from normal conversation
    
    def save(self):
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump({
                "initial_sync_date": self.initial_sync_date,
                "last_followup_date": self.last_followup_date,
                "followup_count": self.followup_count,
                "corrections_made": self.corrections_made,
                "life_changes_detected": self.life_changes_detected,
                "suggested_imports": self.suggested_imports,
                "declined_imports": self.declined_imports,
                "trust_level": self.trust_level,
                "dimensions_unlocked": self.dimensions_unlocked,
                "ongoing_enabled": self.ongoing_enabled,
                "passive_learning": self.passive_learning,
                "pending_confirmations": self.pending_confirmations[-20:],
                "learned_passively": self.learned_passively[-50:],
            }, f, indent=2)
    
    @classmethod
    def load(cls):
        state = cls()
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE) as f:
                    data = json.load(f)
                for k, v in data.items():
                    if hasattr(state, k):
                        setattr(state, k, v)
            except:
                pass
        return state


def detect_life_changes(message: str) -> list[dict]:
    """Scan a message for life change signals."""
    changes = []
    msg_lower = message.lower()
    
    for category, signals in LIFE_CHANGE_SIGNALS.items():
        for signal in signals:
            if signal in msg_lower:
                changes.append({
                    "category": category,
                    "signal": signal,
                    "message_excerpt": message[:200],
                    "detected_at": datetime.now(timezone.utc).isoformat(),
                })
                break  # One per category
    
    return changes


def detect_correction(message: str) -> bool:
    """Check if the user is correcting something about their profile."""
    for pattern in CORRECTION_PATTERNS:
        if re.search(pattern, message, re.IGNORECASE):
            return True
    return False


def should_followup(state: FollowUpState) -> dict:
    """Determine if and what kind of follow-up is appropriate right now."""
    now = datetime.now(timezone.utc)
    
    if not state.initial_sync_date:
        return {"should": False, "reason": "no_initial_sync"}
    
    # If user hasn't been asked about ongoing yet, ask after initial sync
    if state.ongoing_enabled is None:
        return {
            "should": True,
            "type": "opt_in",
            "reason": "first_time_choice",
            "message": None,  # The agent crafts this naturally at the end of initial sync
            "instruction": "At the end of the initial Soulsync setup, naturally ask if they want you to keep learning over time. Something like: 'By the way — want me to keep picking up on things as we chat? I\'ll learn your preferences naturally without asking a bunch of questions. You can turn it off anytime.' Don't make it a big deal. It's a casual offer.",
        }
    
    # If user opted out of ongoing, only respond to explicit corrections
    if not state.ongoing_enabled:
        return {"should": False, "reason": "user_opted_out"}
    
    initial = datetime.fromisoformat(state.initial_sync_date)
    days_since_sync = (now - initial).days
    
    last_followup = None
    if state.last_followup_date:
        last_followup = datetime.fromisoformat(state.last_followup_date)
    
    days_since_followup = (now - last_followup).days if last_followup else days_since_sync
    
    result = {"should": False, "type": None, "reason": None, "message": None}
    
    # Pending confirmations take priority — weave them into natural conversation
    if state.pending_confirmations:
        conf = state.pending_confirmations[0]
        result = {
            "should": True,
            "type": "soft_confirm",
            "reason": "pending_confirmation",
            "confirmation": conf,
            "instruction": f"You picked up that {conf.get('fact', '')} from a recent conversation. Next time it's naturally relevant, casually confirm it. DON'T say 'I noticed you mentioned...' Instead, USE the fact and see if they correct you. Example: if you learned they like hiking, next time they ask about weekend plans, say 'Weather looks good for a hike this weekend' — if they go with it, it's confirmed. If they say 'I don't hike', you learned something.",
        }
        return result
    
    # Week 1: Light touch, woven into normal conversation
    if state.followup_count == 0 and days_since_sync >= 3 and days_since_sync < 10:
        result = {
            "should": True,
            "type": "accuracy_check",
            "reason": "3_days_post_sync",
            "message": None,
            "instruction": "It's been a few days since setup. DON'T send a 'check-in' message. Instead, next time the user asks you something, naturally weave in a reference to something from their profile. If they correct you, update the file. If they don't, you're good. Example: 'Here's that code — kept it concise since that's how you like it.' This implicitly confirms their communication preference without asking.",
        }
    
    # Week 2-3: Offer data imports only if there's a natural opening
    elif state.followup_count == 1 and days_since_sync >= 14 and days_since_sync < 25:
        result = {
            "should": True,
            "type": "data_import_offer",
            "reason": "2_weeks_post_sync",
            "message": None,
            "instruction": "It's been 2 weeks. DON'T send a standalone 'want to connect accounts?' message. Instead, wait for a moment where data imports would naturally help. Example: if they ask about their code, say 'I could answer this better if I could see your GitHub. Want me to connect it? Takes 10 seconds.' Only offer ONE source at a time, and only when relevant.",
        }
    
    # Monthly: Only if there's something to update
    elif days_since_followup >= 30:
        result = {
            "should": True,
            "type": "life_update",
            "reason": "monthly_checkin",
            "message": None,
            "instruction": "It's been a month. DON'T send a formal check-in. Instead, if you notice your profile info might be stale (e.g., they mention something that contradicts their profile), gently update. If nothing seems stale, do nothing. Silence is fine.",
        }
    
    # Trust progression: unlock deeper dimensions naturally
    if state.trust_level == "initial" and state.followup_count >= 2:
        state.trust_level = "comfortable"
    
    return result


def handle_correction(message: str, state: FollowUpState) -> dict:
    """Process a user correction and suggest file updates."""
    state.corrections_made.append({
        "message": message[:200],
        "detected_at": datetime.now(timezone.utc).isoformat(),
    })
    state.save()
    
    return {
        "action": "correction_detected",
        "instruction": (
            "The user is correcting something about their profile. "
            "Read their message carefully, identify what changed, "
            "update the relevant file (USER.md, SOUL.md, or MEMORY.md), "
            "and confirm the change. Example: 'Updated — I've changed your timezone to Pacific.'"
        ),
        "files_to_check": ["USER.md", "SOUL.md", "MEMORY.md", "PERSONALITY.md"],
    }


def handle_life_change(changes: list[dict], state: FollowUpState) -> dict:
    """Process detected life changes and suggest profile updates."""
    state.life_changes_detected.extend(changes)
    state.save()
    
    categories = [c["category"] for c in changes]
    
    prompts = {
        "job": "Sounds like your work situation changed. Want me to update your profile?",
        "location": "New location? I should update your timezone and location info.",
        "relationship": "Life update noted. Want me to update your profile with this?",
        "interests": "New interest detected! Want me to add that to your profile?",
        "technical": "Sounds like your tech setup changed. Want me to update what I know about your stack?",
    }
    
    messages = [prompts.get(c, "") for c in categories if c in prompts]
    
    return {
        "action": "life_change_detected",
        "categories": categories,
        "suggestion": " ".join(messages),
        "files_to_update": ["USER.md", "MEMORY.md"],
    }


def process_message(message: str) -> dict | None:
    """Check any incoming message for follow-up triggers. Returns None if no action needed."""
    state = FollowUpState.load()
    
    # Check for corrections
    if detect_correction(message):
        return handle_correction(message, state)
    
    # Check for life changes
    changes = detect_life_changes(message)
    if changes:
        return handle_life_change(changes, state)
    
    return None


# ─── Passive Learning ─────────────────────────────────────────────────
# Picks up facts from normal conversation without explicitly asking

PASSIVE_PATTERNS = {
    "preference": [
        (r"i (?:really )?(?:love|like|enjoy|prefer|am into)\s+(.+?)(?:\.|$|,|!)", "likes"),
        (r"i (?:hate|dislike|can't stand|don't like|avoid)\s+(.+?)(?:\.|$|,|!)", "dislikes"),
        (r"i(?:'m| am) (?:a )?(morning person|night owl|early bird|vegetarian|vegan)", "trait"),
        (r"my favorite (\w+) is (.+?)(?:\.|$|,)", "favorite"),
    ],
    "context": [
        (r"i(?:'m| am) (?:at|in|visiting|heading to)\s+(.+?)(?:\.|$|,)", "location_mention"),
        (r"my (?:wife|husband|partner|girlfriend|boyfriend|spouse)\s+(\w+)", "partner_name"),
        (r"my (?:kid|son|daughter|child)(?:'s name is| named| called)\s+(\w+)", "child_name"),
        (r"my (?:dog|cat|pet)(?:'s name is| named| called)\s+(\w+)", "pet_name"),
        (r"i work (?:at|for)\s+(.+?)(?:\.|$|,)", "employer"),
        (r"my (solar panels|boat|rv|node|server|printer|tesla)", "possession"),
        (r"i (?:have|own) (?:a|an|some)\s+(.+?)(?:\.|$|,| and| that| which)", "possession"),
    ],
}


def passive_scan(message: str, state: FollowUpState) -> list[dict]:
    """Scan a normal message for personality/preference signals.
    Returns list of facts learned. Does NOT update files — just queues for confirmation."""
    
    if not state.passive_learning:
        return []
    
    learned = []
    msg_lower = message.lower()
    
    for category, patterns in PASSIVE_PATTERNS.items():
        for pattern, fact_type in patterns:
            for match in re.finditer(pattern, message, re.IGNORECASE):
                fact = match.group(1).strip() if match.lastindex == 1 else f"{match.group(1)}: {match.group(2)}".strip()
                
                # Don't re-learn things we already know
                already_known = any(
                    l.get("fact", "").lower() == fact.lower() 
                    for l in state.learned_passively
                )
                if already_known:
                    continue
                
                entry = {
                    "fact": fact,
                    "type": fact_type,
                    "category": category,
                    "source_message": message[:100],
                    "learned_at": datetime.now(timezone.utc).isoformat(),
                    "confirmed": False,
                }
                learned.append(entry)
                state.learned_passively.append(entry)
                
                # Queue for soft confirmation later
                state.pending_confirmations.append(entry)
    
    if learned:
        state.save()
    
    return learned


def set_ongoing(enabled: bool, state: FollowUpState = None):
    """User opts in or out of ongoing personalization."""
    if state is None:
        state = FollowUpState.load()
    state.ongoing_enabled = enabled
    state.save()
    return {"ongoing_enabled": enabled}


def confirm_fact(fact_index: int, confirmed: bool, state: FollowUpState = None):
    """Mark a pending confirmation as confirmed or rejected."""
    if state is None:
        state = FollowUpState.load()
    
    if 0 <= fact_index < len(state.pending_confirmations):
        fact = state.pending_confirmations.pop(fact_index)
        if confirmed:
            fact["confirmed"] = True
            # Update the learned list too
            for l in state.learned_passively:
                if l.get("fact") == fact.get("fact"):
                    l["confirmed"] = True
        else:
            # Remove from learned
            state.learned_passively = [
                l for l in state.learned_passively 
                if l.get("fact") != fact.get("fact")
            ]
        state.save()
        return {"action": "confirmed" if confirmed else "rejected", "fact": fact}
    
    return {"error": "invalid index"}


# ─── CLI ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: followup.py <check|scan|mark-complete|status> [message]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "check":
        state = FollowUpState.load()
        result = should_followup(state)
        print(json.dumps(result, indent=2))
    
    elif cmd == "scan" and len(sys.argv) >= 3:
        message = " ".join(sys.argv[2:])
        result = process_message(message)
        print(json.dumps(result, indent=2) if result else '{"action": "none"}')
    
    elif cmd == "mark-complete":
        state = FollowUpState.load()
        if not state.initial_sync_date:
            state.initial_sync_date = datetime.now(timezone.utc).isoformat()
        state.last_followup_date = datetime.now(timezone.utc).isoformat()
        state.followup_count += 1
        state.save()
        print(json.dumps({"status": "marked", "count": state.followup_count}))
    
    elif cmd == "passive" and len(sys.argv) >= 3:
        message = " ".join(sys.argv[2:])
        state = FollowUpState.load()
        learned = passive_scan(message, state)
        print(json.dumps({"learned": learned, "pending_confirmations": len(state.pending_confirmations)}, indent=2))
    
    elif cmd == "opt-in":
        print(json.dumps(set_ongoing(True)))
    
    elif cmd == "opt-out":
        print(json.dumps(set_ongoing(False)))
    
    elif cmd == "status":
        state = FollowUpState.load()
        print(json.dumps({
            "initial_sync": state.initial_sync_date,
            "last_followup": state.last_followup_date,
            "followup_count": state.followup_count,
            "trust_level": state.trust_level,
            "ongoing_enabled": state.ongoing_enabled,
            "passive_learning": state.passive_learning,
            "corrections": len(state.corrections_made),
            "life_changes": len(state.life_changes_detected),
            "passively_learned": len(state.learned_passively),
            "pending_confirmations": len(state.pending_confirmations),
        }, indent=2))
    
    else:
        print(json.dumps({"error": f"Unknown command: {cmd}"}))
