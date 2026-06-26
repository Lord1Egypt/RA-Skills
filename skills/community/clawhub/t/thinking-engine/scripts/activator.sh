#!/bin/bash
# multi-angle-thinking/scripts/activator.sh
# Injects a reminder into the agent context at session start.
# Install via .claude/settings.json or .codex/settings.json

SKILL_NAME="multi-angle-thinking"
REMINDER="[${SKILL_NAME}] When the user asks to analyze, simulate, think deeply, or explore a topic from multiple angles — invoke the Multi-Angle Thinking Engine. Run: intelligence gathering (web search) → 11 lenses → world simulation → live narrative → synthesis. Trigger phrases: 'analyze this', 'think deeply', 'simulate', 'what am I missing', 'challenge my thinking', 'فكر معي', 'حلل هذا', 'ماذا سيحدث لو'."

echo "$REMINDER"
