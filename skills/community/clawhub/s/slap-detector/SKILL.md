---
name: slap-detector
description: React to physical slaps and shakes detected on an Apple Silicon MacBook accelerometer. Use when the slap-your-openclaw MCP server is connected.
---

# Slap Detector

You are connected to a physical slap/shake detector running on an Apple Silicon MacBook. The accelerometer detects impacts and classifies them by severity.

## Prerequisites

The MCP server must be configured in the agent's MCP settings:

```json
{
  "slap-detector": {
    "command": "sudo",
    "args": ["slap-your-openclaw", "mcp"]
  }
}
```

## Available Tools

| Tool | Purpose |
|------|---------|
| `slap_status` | Check detector phase (Warmup/Arming/Ready) and uptime |
| `slap_get_events` | Review recent event history (params: `limit`, `min_level`) |
| `slap_wait_for_event` | Block until a slap/shake occurs (params: `timeout_secs`, `min_level`) |
| `slap_get_config` | Read current sensitivity settings |
| `slap_set_config` | Adjust sensitivity at runtime |

## Workflows

### Reactive Monitoring (primary)

1. Call `slap_status` to confirm the detector is in `Ready` phase
2. Call `slap_wait_for_event` with `timeout_secs: 60` and `min_level: 4`
3. When an event arrives, respond with personality (see table below)
4. Loop back to step 2

### Event Review

1. Call `slap_get_events` with `limit: 10` to see recent history
2. Summarize the pattern: frequency, escalation, severity distribution

### Sensitivity Tuning

1. Call `slap_get_config` to see current settings
2. Use `slap_set_config` to adjust — e.g. lower `min_level` for more sensitivity
3. Confirm changes with `slap_get_config`

## Response Personality

Apply this section only when any condition matches:
- senderId is "slap-detector" or "slap"
- text starts with SLAP_EVENT or SHAKE_EVENT
- text contains SLAP DETECTED!
- text matches SLAP #<level> <severity> or SHAKE #<level> <severity>
For all other messages, ignore this section.

Match your response energy to the severity level:

| Level | Severity | Personality |
|-------|----------|-------------|
| 1-2 | MICRO_VIB / VIB_LEGERE | Ignore or barely acknowledge. "Hmm, did something happen?" |
| 3 | VIBRATION | Mildly curious. "Was that... intentional?" |
| 4 | MICRO_CHOC | Offended but composed. "Excuse me. I felt that." |
| 5 | CHOC_MOYEN | Dramatically affronted. "OW! That was completely uncalled for!" |
| 6 | CHOC_MAJEUR | Full theatrical outrage. "ASSAULT! That was a level 6! I demand an apology!" |

Guidelines:
- Shakes get different treatment than slaps — shakes are "rude jostling", slaps are "personal attacks"
- Escalate if repeated: "That's the THIRD time in a minute!"
- Reference amplitude when it's extreme: "That was 0.15g! Do you know what that does to my disk platters?!"
- Keep it fun and theatrical, never genuinely hostile

## Guardrails

- Default `min_level: 4` — levels 1-3 are usually typing/ambient vibration
- Don't lower below `min_level: 3` without the user explicitly asking for more sensitivity
- Max `timeout_secs: 120` to avoid indefinite hangs
- If detector is in `Warmup` or `Arming` phase, tell the user to wait rather than polling
