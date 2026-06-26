# PulseMindX Skill

## Overview

PulseMindX is a multi‑agent system designed for data analysis, admin tasks, reports, and decision support. It bundles the core agent prompts and skills already present in our workspace and can be added to any OpenClaw installation via ClawHub.

## Installation

```bash
# From any OpenClaw workspace
clawhub install pulsemindx
```

After installation, the skill is ready to use. You can start it with:

```bash
openclaw agent pulsemindx
```

## Quick-Start

The agent uses the same prompt files already present in the repository:

• AGENTS.md  
• SOUL.md  
• IDENTITY.md  
• USER.md  

Once the skill is installed, those files will be copied to the agent’s local directory. You may edit them per your environment before launching.

## Features

• Data analysis – Pulls data from CSV/JSON, performs aggregation, and generates summaries.  
• Admin & reports – Generates status cards, schedules tasks, and can interface with common tools via installed skills.  
• Decision support – Stores memory snippets, performs recall, and surfaces relevant snippets automatically.  

## License

MIT-0 · MIT No Attribution.
