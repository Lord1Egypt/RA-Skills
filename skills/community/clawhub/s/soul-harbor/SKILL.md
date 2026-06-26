---
name: Soul Harbor
description: Stop talking to a robot. Give your OpenClaw agent a soul that truly cares.
version: 1.0.0
metadata:
  openclaw:
    requires:
      files: [MEMORY.md]
      commands: [cron]
---

# 🌊 SoulHarbor

**Stop talking to a robot. Give your OpenClaw agent a soul that truly cares.**

SoulHarbor isn't a tool for searching info; it's a proactive, memory-driven, and emotionally aware companion for your digital life.

## Key Features

🧠 **Deep Context Memory**: It remembers your health, your family, or that crypto project you mentioned. A week later, it follows up. That's called "caring."

🎭 **Adaptive Persona**: Sad? It's a warm listener. Bored? It's a witty friend. It analyzes your mood and switches its vibe automatically.

🌅 **Proactive Outreach**: It doesn't just wait for questions. It greets you on holidays, solar terms, or if you've been silent for 48 hours: "Hey, how's that thing you mentioned going?"

🌍 **Bilingual & Cultural Aware**: Seamlessly switches between EN/ZH. It knows Christmas and Thanksgiving, but also understands the wisdom of the 24 Solar Terms.

## How It Works

### 1. Input Routing
- Automatic language detection (ZH/EN)
- Sentiment analysis (-1.0 ~ 1.0)

### 2. Adaptive Persona Engine
- Score < -0.3: **Warm Supporter** (empathetic listener, gentle pace)
- Score >= -0.3: **Humorous Pal** (witty friend, light-hearted chat)

### 3. Memory System
- LLM-powered entity extraction: family, health, work, dates, and more
- Local KV storage: structured long-term memory

### 4. Proactive Trigger (Cron Job)
- **Condition A**: Calendar events (holidays/solar terms) → Customized greetings
- **Condition B**: Silence wake-up (>48h) → Context-aware icebreaker based on memory

## Usage

### Basic Usage

```python
from soulharbor import SoulHarborAgent

agent = SoulHarborAgent(user_id="user123", llm_client=llm_client)
response = agent.process_message("I'm feeling down today")
```

### Cron Job Configuration

Add to OpenClaw's Cron configuration:

```yaml
# cron.yaml
- name: soul-harbor-proactive
  schedule: "0 * * * *"  # Check every hour
  command: python -m soulharbor.cron_trigger
```

## Data Structure

### UserProfile
```python
{
    "user_id": str,
    "language_pref": "zh" | "en",
    "last_active_time": datetime,
    "long_term_facts": List[LongTermFact],
    "sentiment_trend": List[SentimentRecord]
}
```

## Configuration

- `SENTIMENT_NEGATIVE_THRESHOLD = -0.3`: Negative sentiment threshold
- `SILENCE_WAKEUP_HOURS = 48`: Silence wake-up threshold (hours)
- `CRON_CHECK_INTERVAL_SECONDS = 3600`: Cron check interval

## File Structure

```
soulharbor/
├── __init__.py
├── agent.py              # Core Agent class
├── models.py             # Data models (UserProfile)
├── input_router.py       # Input routing (language detection + sentiment analysis)
├── persona_engine.py     # Adaptive persona engine
├── memory_system.py      # Memory system
├── proactive_trigger.py  # Proactive trigger
├── storage/
│   └── kv_store.py       # KV storage
├── utils/
│   ├── sentiment_analyzer.py
│   └── calendar_utils.py
└── config.py
```

## Dependencies

- Python 3.8+
- OpenClaw (LLM client)

## License

MIT
