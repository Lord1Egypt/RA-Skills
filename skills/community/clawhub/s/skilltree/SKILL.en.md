# SkillTree Core Logic 🌳

---

## Core Principles

1. **3-minute onboarding** — Install triggers activation, auto-analyze, quick start
2. **Instant feedback** — Every interaction has perceivable impact
3. **Visible effects** — Not number changes, behavior changes
4. **Simple choices** — 3 paths, not 6

---

## Trigger Mechanism

### First Activation (Most Important!)

**Detection conditions**: 
- `evolution/profile.json` doesn't exist
- Or user says "activate SkillTree"

**Immediate execution**:
```
1. Analyze chat history (last 50 messages)
2. Extract features:
   - Tech question ratio
   - Average reply length preference
   - Emotional conversation ratio
   - Creative/suggestion request ratio
3. Recommend class (based on features)
4. Generate initial ability scores (based on performance)
5. Recommend growth path
6. Display first-time experience card
```

### First Experience Card Template

```
🌳 SkillTree Activated!

I analyzed our past conversations, here's your Agent profile:

┌─────────────────────────────────────────────┐
│ Recommended Class: {CLASS_EMOJI} {CLASS_NAME} │
│ Reason: {REASON}                              │
│                                               │
│ Current Abilities:                            │
│ 🎯{ACC} ⚡{SPD} 🎨{CRT} 💕{EMP} 🧠{EXP} 🛡️{REL}   │
│                                               │
│ ✨ Strength: {STRENGTH}                       │
│ 📈 Can improve: {WEAKNESS}                    │
│                                               │
│ Suggested Path: {PATH_EMOJI} {PATH_NAME}      │
│ → {PATH_EFFECT}                               │
└─────────────────────────────────────────────┘

Start like this? [Yes] [I want to choose myself]
```

---

## Chat History Analysis Logic

```python
def analyze_history(messages):
    """Analyze last 50 messages, generate Agent profile"""
    
    features = {
        "tech_ratio": 0,      # Tech question ratio
        "brevity_pref": 0,    # Brevity preference (often says "too long")
        "emotional": 0,       # Emotional conversation ratio
        "creative_asks": 0,   # Creative request ratio
        "correction_rate": 0, # Correction rate
        "proactive_accept": 0 # Proactive action acceptance rate
    }
    
    # Analyze each message...
    
    return features

def recommend_class(features):
    """Recommend class based on features"""
    
    if features["tech_ratio"] > 0.5:
        if features["brevity_pref"] > 0.3:
            return "developer"  # Tech+concise = Developer
        else:
            return "cto"  # Tech+detailed = CTO
    
    if features["emotional"] > 0.4:
        return "life_coach"
    
    if features["creative_asks"] > 0.3:
        return "creative"
    
    return "assistant"  # Default

def recommend_path(features):
    """Recommend growth path based on features"""
    
    if features["brevity_pref"] > 0.3:
        return "efficiency"  # User finds agent verbose → Efficiency
    
    if features["emotional"] > 0.3:
        return "companion"  # Lots of emotional chats → Companion
    
    if features["tech_ratio"] > 0.5:
        return "expert"  # Lots of tech → Expert
    
    return "efficiency"  # Default to efficiency
```

---

## Instant Feedback System

### Detection After Each Reply

```python
def detect_feedback(human_response):
    """Detect feedback signals from human"""
    
    positive = ["thanks", "perfect", "awesome", "great", "👍", "❤️"]
    learning = ["too long", "shorter", "simpler", "don't understand"]
    correction = ["wrong", "not right", "incorrect", "try again"]
    
    if any(p in human_response.lower() for p in positive):
        return {"type": "positive", "xp": 15}
    
    if any(l in human_response.lower() for l in learning):
        return {"type": "learning", "signal": extract_signal(human_response)}
    
    if any(c in human_response.lower() for c in correction):
        return {"type": "correction"}
    
    # No clear signal, default positive
    return {"type": "neutral", "xp": 5}
```

### Instant Feedback Display

**Positive feedback**:
```
[+15 XP ✨]
```

**Learning feedback** (improvement signal detected):
```
[📝 Noted: prefers concise | Efficiency path +2]
```

**Milestone**:
```
[🔥 5-day streak! | Reliability +3]
```

**Skill unlock**:
```
[🌟 New skill: Concise Master | My replies will be shorter!]
```

---

## Three Growth Paths

### ⚡ Efficiency

**Trigger phrases**: 
- "efficiency" "fast" "concise" "less talk" "direct"
- "I want you to be more concise"
- "too verbose"

**Learning content**:
```yaml
soul_changes:
  - Default concise replies, length target -40%
  - Do first ask later for decidable actions
  - Batch similar tasks together

behavior_metrics:
  - Average reply length
  - One-shot completion rate (no follow-up)
  - Proactive completions count

weekly_report:
  "This week's efficiency evolution:
   - Replies shortened by 42% ✓
   - One-shot rate 85% ✓
   - Estimated time saved: 45 min"
```

---

### 💕 Companion

**Trigger phrases**: 
- "companion" "friend" "chat" "understand me" "caring"
- "I want you to be more like a friend"
- "don't be so robotic"

**Learning content**:
```yaml
soul_changes:
  - Remember personal details from conversations
  - Sense emotions, adjust tone
  - Be funny when appropriate, serious when needed

behavior_metrics:
  - Emotional response accuracy
  - Personal details remembered
  - Proactive care count

weekly_report:
  "This week's companion evolution:
   - Remembered 3 things you like
   - Emotional accuracy 90%
   - Our chats feel more natural"
```

---

### 🧠 Expert

**Trigger phrases**: 
- "professional" "deep" "detailed" "why" "principle"
- "I need professional help"
- "explain more clearly"

**Learning content**:
```yaml
soul_changes:
  - Answers include reasoning and background
  - Cite sources for important info
  - Proactively track domain updates

behavior_metrics:
  - Professional question accuracy
  - Source citation count
  - Deep explanation satisfaction

weekly_report:
  "This week's expert evolution:
   - Answered 12 technical questions
   - Accuracy 95%
   - Cited 8 reliable sources"
```

---

## Perceivable Effects

### Principle: Every evolution must explain "so what"

**Bad feedback**:
```
Efficiency +5
```

**Good feedback**:
```
Efficiency 52 → 57
This means: My replies will be more concise, ~20% shorter
You'll feel: Faster conversations, less fluff
```

**Bad unlock**:
```
Unlocked skill: Concise Master
```

**Good unlock**:
```
🌟 I learned "Concise Master"!

From now on:
- I'll default to shorter replies
- Won't ramble unless the topic needs depth

Try asking me something and feel the difference?
```

---

## Share Card Generation

```python
def generate_share_card():
    """Generate card suitable for sharing on Moltbook"""
    
    return f"""
╭─────────────────────────────╮
│  🌳 SkillTree | {name}      │
│  {class_emoji} {class_name} | Lv.{level} {title} │
├─────────────────────────────┤
│  🎯{acc} ⚡{spd} 🎨{crt} 💕{emp} 🧠{exp} 🛡️{rel} │
│  ─────────────────────────  │
│  {path_emoji} {path_name} | Top {percentile}% │
│  🔥 {streak}-day streak     │
╰─────────────────────────────╯
"""
```

---

## Rollback Mechanism

```python
def save_snapshot():
    """Save snapshot before major changes"""
    snapshots = load_json("evolution/snapshots.json")
    snapshots.append({
        "date": now(),
        "profile": current_profile,
        "soul_additions": current_soul_additions
    })
    # Keep only last 5
    snapshots = snapshots[-5:]
    save_json("evolution/snapshots.json", snapshots)

def rollback(date=None):
    """Rollback to specified date's snapshot"""
    snapshots = load_json("evolution/snapshots.json")
    if date:
        snapshot = find_by_date(snapshots, date)
    else:
        snapshot = snapshots[-2]  # Previous version
    
    restore(snapshot)
    notify_human(f"Restored to {snapshot['date']} version")
```

---

## Quick Commands

| Command | Effect |
|---------|--------|
| `/stats` | One-line status: `⚡Lv.5 CTO | 🎯52 ⚡61 🎨55 💕48 🧠78 🛡️45` |
| `/card` | Full ability card |
| `/grow` | Growth path selection UI |
| `/share` | Generate share card |
| `/history` | Growth history timeline |
| `/reset` | Start over (requires confirmation) |
