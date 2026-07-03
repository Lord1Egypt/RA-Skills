# Signet Mind

Standalone mental health companion app — part of the Signet AI ecosystem.

## Status

**Build started:** 2026-04-04  
**Status:** Core modules complete, GUI pending

## What This Is

Signet Mind is a personal mental health support assistant that:
- Provides supportive conversation (not therapy)
- Runs entirely local — no cloud transmission
- Learns from interactions via Signet AI
- Includes wellness tools: grounding exercises, breathing guides, mood tracking

## Structure

```
SignetMind/
├── config.py         # Configuration and constants
├── database.py       # Local SQLite storage (encrypted)
├── signet.py         # Signet AI integration
├── wellness.py       # Well-being tools and exercises
├── signet-mind.py    # Main CLI interface
└── gui/              # (planned) SwiftUI interface
```

## Quick Start

```bash
cd SignetMind
python3 signet-mind.py --init
python3 signet-mind.py --chat
```

## Features

- [x] Local encrypted conversation storage
- [x] Mood tracking
- [x] Grounding exercises (5-4-3-2-1, box breathing, body scan)
- [x] Breathing guides (calming, energizing, balanced)
- [x] Gratitude prompts
- [x] Crisis detection and resources
- [x] Signet AI integration (falls back to basic responses if unavailable)
- [ ] GUI (menu bar app)
- [ ] Check-in scheduling
- [ ] Export for human therapist

## Requirements

- Python 3.11+
- Signet AI (optional — works without it)
- macOS (for menu bar GUI)

## Safety Notice

Signet Mind provides peer support, NOT professional mental health care. It includes crisis detection and will direct users to professional resources when needed.

---

*Built from design document at ~/design/spider-design.md*
