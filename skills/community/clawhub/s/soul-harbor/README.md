# 🌊 SoulHarbor

**Stop talking to a robot. Give your OpenClaw agent a soul that truly cares.**

A bilingual (EN/ZH) proactive companion Skill for OpenClaw, powered by state machine + memory + scheduled tasks to deliver a humanized emotional companion.

## Project Structure

```
SoulHarbor/
├── SKILL.md                    # OpenClaw Skill metadata
├── README.md                   # Project documentation
├── requirements.txt            # Dependencies
├── soulharbor/
│   ├── __init__.py
│   ├── agent.py               # Core Agent class
│   ├── models.py              # Data models (UserProfile)
│   ├── input_router.py        # Input routing (language detection + sentiment analysis)
│   ├── persona_engine.py      # Adaptive persona engine
│   ├── memory_system.py       # Memory system
│   ├── proactive_trigger.py   # Proactive trigger
│   ├── cron_trigger.py        # Cron Job entry point
│   ├── config.py              # Configuration
│   ├── storage/
│   │   ├── __init__.py
│   │   └── kv_store.py        # KV storage implementation
│   └── utils/
│       ├── __init__.py
│       ├── sentiment_analyzer.py
│       └── calendar_utils.py
└── data/                      # Data storage directory (auto-created)
```

## Core Modules

### 1. SoulHarborAgent (`agent.py`)
Main entry class that integrates all modules:
- `process_message(text)` - Process user messages
- `get_system_prompt()` - Get dynamic system prompt
- `trigger_proactive_check()` - Trigger proactive check

### 2. MemorySystem (`memory_system.py`)
Memory system core interface:
- `extract_entities()` - LLM-powered entity extraction
- `add_conversation_memory()` - Add conversation memory
- `get_memory_for_proactive_message()` - Get icebreaker memory

### 3. ProactiveTrigger (`proactive_trigger.py`)
Proactive trigger core interface:
- `check_calendar_events()` - Condition A: Calendar events
- `check_silence_wakeup()` - Condition B: Silence wake-up
- `start_cron_job()` - Start scheduled task

## Quick Start

```python
from soulharbor import SoulHarborAgent

# Initialize (requires OpenClaw LLM client)
agent = SoulHarborAgent(user_id="user123", llm_client=llm_client)

# Process message
response = agent.process_message("I'm feeling down today")
print(response)

# Trigger proactive check
messages = agent.trigger_proactive_check()
```

## Cron Job Configuration

Configure scheduled tasks in OpenClaw:

```bash
# Check every hour
python -m soulharbor.cron_trigger
```

## Data Model

### UserProfile
```python
{
    "user_id": str,
    "language_pref": Language.ZH | Language.EN,
    "last_active_time": datetime,
    "long_term_facts": List[LongTermFact],
    "sentiment_trend": List[SentimentRecord]
}
```

## Features

- ✅ Automatic language detection (EN/ZH)
- ✅ Sentiment analysis (-1.0 ~ 1.0)
- ✅ Adaptive persona switching (Warm Supporter / Humorous Pal)
- ✅ Structured memory extraction (family, health, work, dates)
- ✅ Proactive triggering (holiday greetings + silence wake-up)

## License

MIT
