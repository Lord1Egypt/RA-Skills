# 🦞 Speech Coach — AI Public Speaking Trainer

An AI-powered public speaking coach built on the Dazhao Eloquence Training System. Provides a structured 15-step progressive curriculum, 25 core methodologies, scenario-based practice, and personalized progress tracking — all through natural **text conversation**.

## Text-Only Design

This skill is designed for **pure text-based AI** with no audio or video processing. Body language training (Steps 01-06) uses a unique "**Knowledge Quiz + Script Annotation**" approach:
- AI teaches concepts and tests understanding through quizzes
- Users annotate their speech scripts with markup symbols (`//` for pauses, `**word**` for emphasis, `【手势:描述】` for gestures, etc.)
- AI evaluates whether annotations are logical and well-placed
- Offline homework (mirror practice, video self-review) bridges the gap to physical skills

## Features

- **15-Step Progressive Curriculum** — From body language awareness to full-length impromptu speeches, organized into 4 modules across 2 phases
- **25 Core Methodologies** — Battle-tested techniques including Pyramid Structure, Golden Three Points, STAR Storytelling, Parachute Method, and more
- **Script Annotation System** — Unique markup notation for designing pauses, emphasis, gestures, eye contact, and expressions in text
- **Personalized Coaching** — Adapts practice scenarios to user's occupation (tech, sales, management, education, entrepreneurship)
- **7-Dimension Scoring** — Annotation design, structure, logic, storytelling, improvisation, persuasion, method knowledge
- **Progress Tracking** — Automated step unlocking, milestone achievements, weekly reports with trend analysis
- **Psychological Support** — Built-in modules for handling stage fright, self-doubt, and impatience

## Training System Overview

### Phase 1: Foundation

| Module | Steps | Focus |
|--------|-------|-------|
| Module 1: Overcome Stage Fright | Step 01-06 | Body language awareness — posture, eye contact, gestures, voice design, expression, integrated annotated intro |
| Module 2: Clear Expression | Step 07-10 | Speech structure — Pyramid thinking, Golden Three Points, storytelling, themed speech |

### Phase 2: Application

| Module | Steps | Focus |
|--------|-------|-------|
| Module 3: Impromptu Speaking | Step 11-14 | Real-world scenarios — top-down analysis, bottom-up storytelling, toasts & compliments, constructive criticism |
| Module 4: Graduation | Step 15 | 5-minute comprehensive speech with Q&A |

## Installation

```bash
clawhub install speech-coach
```

Or manually copy the `speech-coach` folder to `~/.openclaw/skills/`.

## Usage

Simply start a conversation with your OpenClaw agent:

> "I want to practice public speaking"
> "Help me prepare for a presentation"
> "I get nervous when speaking in front of people"

The coach will:
1. Conduct an initial assessment (first session only)
2. Guide you through the current training step
3. Provide a tailored practice scenario
4. Score your performance across 7 text-evaluable dimensions
5. Track your progress and unlock the next step when ready

### Script Annotation Symbols

| Symbol | Meaning | Example |
|--------|---------|---------|
| `//` | Short pause | "Ladies and gentlemen // today I want to share..." |
| `///` | Long pause (suspense) | "And the result was? ///" |
| `**word**` | Emphasis | "This is the **most critical** step" |
| `〈slow〉...〈/slow〉` | Slow down | "〈slow〉Remember these three words〈/slow〉" |
| `【gesture:desc】` | Gesture note | "First 【gesture:raise index finger】" |
| `【eye:desc】` | Eye contact note | "【eye:scan left audience】What do you think?" |

### CLI Commands (Progress Tracker)

```bash
# View overall training status
python progress_tracker.py status

# Record a training score (7 dimensions)
python progress_tracker.py score --step 1 \
  --annotation 7 --structure 6 --logic 6 \
  --storytelling 5 --improvisation 5 \
  --persuasion 6 --knowledge 8 \
  --note "Good concept understanding"

# View step details
python progress_tracker.py step-detail --step 3

# Unlock next step
python progress_tracker.py unlock --step 2

# Generate weekly report
python progress_tracker.py report

# View milestones
python progress_tracker.py milestones
```

## 7 Scoring Dimensions

| Dimension | What AI Evaluates |
|-----------|------------------|
| Annotation | Quality of script markup — pauses, emphasis, gestures placed correctly |
| Structure | Speech organization — pyramid, golden 3 points, clear framework |
| Logic | Argument coherence, evidence support, reasoning flow |
| Storytelling | Narrative arc, emotional hooks, vivid details, STAR method |
| Improvisation | Quick thinking, framework application under time pressure |
| Persuasion | Convincingness, audience awareness, call-to-action clarity |
| Knowledge | Understanding of methods — quiz answers, concept explanation |

## Milestones

| Milestone | Condition |
|-----------|-----------|
| 🎉 First Session Complete | Complete 1 training session |
| 💪 Stage Fright Conquered | Complete Module 1 (Steps 1-6) |
| 🧠 Clear Thinker | Complete Module 2 (Steps 7-10) |
| ⚡ Improv Ready | Complete Module 3 (Steps 11-14) |
| 🎓 Graduated | Pass all 15 steps |
| 🔥 10 Sessions | Sustain 10 training sessions |
| 🏆 20 Sessions | Sustain 20 training sessions |
| ⭐ Perfect Score | Achieve 10/10 in any dimension |
| 🌟 All-Around Excellence | Score 7+ in all 7 dimensions |

## File Structure

```
speech-coach/
├── skill.yaml             # Skill metadata
├── SKILL.md               # Coaching protocol (core, indexed by ClawHub)
├── curriculum.md           # Full 15-step curriculum + 25 methods + psychology module
├── progress_tracker.py     # Progress tracking system
└── README.md               # This file
```

## Requirements

- Python 3.9+
- OpenClaw 2026.3+
- No external dependencies (stdlib only)

## License

MIT License — Help everyone speak with confidence!
