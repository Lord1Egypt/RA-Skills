# Skill Creator Assistant

🤖 An AI-powered tool that helps non-technical users create their own OpenClaw skills through guided conversation.

## What It Does

No coding required — just describe what you want, and this skill will:

1. Ask you 5-8 targeted questions about your idea
2. Generate a complete, ready-to-use `SKILL.md`
3. Optionally upload to GitHub

## Quick Start

Upload this skill to your OpenClaw workspace and activate it. Then describe your idea:

> "I want a skill that helps me track competitor pricing"

The assistant will guide you through defining:
- What it should do
- When to trigger it
- What inputs/outputs it needs
- Any limitations

## Generated Output

A properly formatted `SKILL.md` following OpenClaw conventions, including:
- Capability descriptions
- Trigger conditions
- Workflow steps
- Input/output specifications
- Limitations and dependencies

## Upload to GitHub

After generating, the assistant can create a GitHub repo and upload your skill:
1. `gh repo create my-skill`
2. Upload SKILL.md + README.md
3. Share the repo URL

## Example Conversations

**Input:** "I need to monitor social media for my brand mentions"

**Output:** A fully-formed social media monitoring skill with:
- Periodic check workflow
- Alert thresholds
- Multi-platform aggregation

---

Made with ⚡ by 阿信 · OpenClaw
