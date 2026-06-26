# Zeelin Auto Evolution

Version: `0.1.0`

English | [简体中文](README.zh-CN.md)

## Overview
Zeelin Auto Evolution adds a safe, self-improving feedback loop to an agent system. It silently captures corrective user feedback, turns repeated issues into rule proposals, suggests improvements for low-performing skills, and proposes new skills when repeated workflows are not covered. It is intentionally conservative: it can observe automatically, but it must ask for confirmation before changing rules or skills.

## What It Does
- Silently captures corrective feedback from user conversations
- Aggregates repeated feedback into candidate rules
- Scores skill executions across accuracy, coverage, efficiency, and satisfaction
- Suggests skill improvements when performance stays low
- Suggests creating new skills when a repeated pattern has no existing coverage

## Multilingual Support
This `0.1.0` version supports both Chinese and English feedback signals.

Examples of supported Chinese signals:
- `不是这样`
- `你又忘了`
- `不对`
- `我不是让你这么干`

Examples of supported English signals:
- `that's not right`
- `you forgot again`
- `this is wrong`
- `that's not what I asked`
- `don't do it this way`

Detection is implemented in [scripts/detect_feedback_signal.py](scripts/detect_feedback_signal.py).

## Trigger Model
The skill is designed around two automatic checkpoints:

1. Per-message detection
When a user sends a message, a hook or controller can run the detection script. If the message contains corrective feedback, the controller should finish the current task first and then quietly dispatch a `feedback-observer`.

2. Session-start evolution scan
At session start, or when the user explicitly asks to check evolution proposals, the controller can run [scripts/evolution_runner.py](scripts/evolution_runner.py) to scan accumulated feedback and generate proposals.

## Evolution Layers
1. Silent feedback capture
2. Rule graduation after repeated occurrences
3. Skill optimization from low scores
4. New skill proposals for uncovered repeated workflows

## Repository Structure

```text
auto_evolution_skill/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── REFERENCE_ARCHITECTURE.md
├── EXAMPLES.md
├── scripts/
│   ├── detect_feedback_signal.py
│   └── evolution_runner.py
└── templates/
    ├── feedback_index_template.md
    └── feedback_topic_template.md
```

## Quick Start
1. Connect the detection script to your message-submit hook.
2. Dispatch a `feedback-observer` when corrective feedback is detected.
3. Store structured feedback in `.claude/feedback/`.
4. Run `evolution_runner.py` at session start or on demand.
5. Show proposals to the user before applying any rule or skill change.

## Related Files
- [SKILL.md](SKILL.md): core skill behavior and workflow
- [REFERENCE_ARCHITECTURE.md](REFERENCE_ARCHITECTURE.md): architecture and decision rules
- [EXAMPLES.md](EXAMPLES.md): example scenarios and outputs
- [README.zh-CN.md](README.zh-CN.md): Chinese documentation

## Notes
- This release does not auto-edit rules.
- The skill is event-driven, not a background daemon.
- High-quality routing still depends on your controller or hook integration.

## Changelog
- `0.1.0` (2026-04-20): Added English support, split README into English and Chinese versions, and prepared the package for open-source publishing.
