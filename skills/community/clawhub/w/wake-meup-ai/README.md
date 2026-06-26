# wake-meup-ai

Schedule personalized AI wake-up phone calls via wake.meup.ai. Use when a user wants to be woken up by a phone call, schedule morning calls, or set up recurring wake-up calls. Handles phone verification, call scheduling, voice selection, and x402 USDC payment.

## Quick Start

1. Add this skill directory to your agent
2. The agent reads `SKILL.md` for instructions and API documentation
3. Use `scripts/wake-cli.py` for automated x402 payment handling:

```bash
uv run scripts/wake-cli.py --help
```

## Requirements

Requires uv (https://docs.astral.sh/uv/) and a Solana keypair with USDC

## Files

- `SKILL.md` — Skill manifest with API docs and workflow instructions
- `scripts/wake-cli.py` — Reference client with x402 payment handling
- `README.md` — This file
