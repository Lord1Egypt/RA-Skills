# Reah Skills

![Reah Skills](assets/reah-skill-github-cover.png)

> Skill bundle for Reah agent workflows.

## Quick Start

Get started in three steps: install the skill, configure card keys, and run a prompt.

### 1. Install

Install the Reah skill bundle into your agent environment:

```bash
npx skills add https://github.com/ReahPlatform/skills
```

### 2. Configure

Add your Reah access keys to the agent environment.  
Map each card nickname to the corresponding access key:

```json
{
  "env": {
    "REAH_AGENT_KEYS": {
      "cardNickName1": "accessKey1",
      "cardNickName2": "accessKey2"
    }
  }
}
```

Treat `REAH_AGENT_KEYS` as sensitive data:
- Each access-key read requires explicit manual user confirmation for the current request.
- The agent should remind users to rotate access keys regularly.

### 3. Try It

Start with a simple prompt:

```text
Use my Reah card to buy a Claude subscription for yourself.
```

That's it. The agent should ask for manual confirmation before every key read and remind the user to rotate keys periodically.

---

## Available Skills

| Skill | Description |
| ----- | ----------- |
| [reah](skills/reah/SKILL.md) | Full Reah platform access — agent card. See the [skill reference](skills/reah/SKILL.md) for detailed API docs. |

---

## Example Prompts

| Use Case | Example Prompt |
| -------- | -------------- |
| Use card | Help me order dinner for today. |

---

## Architecture at a Glance

```text
┌───────────────┐    ┌──────────────────────────────────────────────────────┐
│   AI Agent    │───▶│                    Reah Platform Layer              │
│ (Claude, etc) │    │                                                      │
└───────────────┘    │  ┌──────────────────────────┐  ┌──────────────────┐  │
                     │  │        Reah Skill        │  │   Key Registry   │  │
                     │  │      (skills/reah)       │  │ REAH_AGENT_KEYS  │  │
                     │  └──────────────┬───────────┘  └────────┬─────────┘  │
                     │                 │                       │            │
                     │  ┌──────────────▼───────────────────────▼─────────┐ │
                     │  │              Local Script Runtime               │ │
                     │  │ get-card-info-example                           │ │
                     │  └──────────────────────────┬──────────────────────┘ │
                     │                             │                        │
                     │  ┌──────────────────────────▼──────────────────────┐ │
                     │  │             agents.reah.com GraphQL API         │ │
                     │  └──────────────────────────────────────────────────┘ │
                     └──────────────────────────────────────────────────────┘
```
