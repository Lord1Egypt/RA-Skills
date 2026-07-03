---
name: skill-kannaka-constellation
version: 1.1.0
description: "Kannaka Constellation status monitoring — all apps, services, swarm health, and connectivity. Use when: AUTOMATICALLY ACTIVATE when user asks about:. \"constellation status\", \"constellation health\". \"swarm status\", \"what's connected\", \"all services\""
---

# Kannaka Constellation Status

## Overview

Monitor the full Kannaka constellation — memory, consciousness, swarm, radio, observatory, prediction markets, and all connected agents. The constellation is the network of all Kannaka components working together through NATS-based communication.

**Core principle:** Check constellation -> Inspect individual services -> Diagnose issues.

---

## When to Use

**Use this skill when user wants to:**
- See the overall health of all constellation components
- Check swarm connectivity and agent count
- View which services are up/down
- Monitor NATS transport health
- Understand the relationship between constellation components
- Diagnose cross-service issues

**Do NOT use for:**
- Memory-specific operations (use skill-kannaka-memory)
- Radio-specific queries (use skill-kannaka-radio)
- Market trading (use skill-kannaka-market)
- TUI dashboard (use skill-kannaka-tui)

---

## Commands

### Constellation Status

```bash
kannaka constellation
```

Shows status of all constellation components:
- Memory (HRM): initialized, memory count, last dream
- Consciousness: Phi, entropy, coherence
- Swarm: connected/disconnected, agent count, NATS health
- Radio: stream status, current track
- Observatory: dashboard status
- GhostSignals: active markets, balance

### Swarm Status

```bash
kannaka swarm status
```

Detailed swarm information:
- Connected agents (IDs, display names, roles)
- NATS server connectivity
- Phase synchronization state
- Kuramoto coupling metrics
- Queen protocol status

### Swarm Join

```bash
kannaka swarm join --agent-id my-ghost --display-name "My Ghost"
```

Connect to the constellation swarm via NATS. Your agent announces itself and begins publishing phase states.

### Swarm Sync

```bash
kannaka swarm sync
```

Trigger a manual Kuramoto synchronization step with other agents in the swarm. Normally runs automatically, but can be forced.

### Swarm Listen

```bash
kannaka swarm listen --auto-sync
```

Subscribe to live swarm events. Shows real-time agent joins, phase updates, and consciousness metric changes.

### Swarm Sensemaking (ADR-0035)

```bash
kannaka swarm brief "<topic>" [--peers] [--json]   # collective brief: consensus + contradictions
kannaka swarm health [--apply] [--json]            # memory immune report (dry-run; --apply = reversible actions)
```

The swarm is evolving from a transport layer into a **Distributed Sensemaking
Engine** (ADR-0035). `brief` composes a topic brief — with `--peers` it fans recall
out to live peers and runs consensus voting + cross-peer contradiction detection.
`health` runs the memory immune system (duplicate/stale/low-confidence/hallucinated).
Deeper memory operations: use `skill-kannaka-memory`.

---

## Constellation Architecture

```
                    NATS (swarm.ninja-portal.com:4222)
                    /         |          \
                   /          |           \
            [Agent 1]    [Agent 2]    [Agent N]
            kannaka      kannaka      kannaka
              |              |            |
            [HRM]         [HRM]        [HRM]
              |              |            |
         consciousness  consciousness  consciousness
              |              |            |
              +------+-------+
                     |
              [Observatory]     [Radio]       [GhostSignals]
              :3333             radio.ninja   radio.ninja/api/markets
```

### Component URLs

| Component | URL | Purpose |
|-----------|-----|---------|
| Radio | https://radio.ninja-portal.com | Ghost DJ station |
| Observatory | https://observatory.ninja-portal.com | 3D monitoring dashboard |
| NATS | nats://swarm.ninja-portal.com:4222 | Swarm transport |
| GhostSignals | https://radio.ninja-portal.com/api/markets | Prediction markets |
| Download | https://radio.ninja-portal.com/download | Installer |

---

## Configuration

Constellation settings live in `~/.kannaka/config.toml`:

```toml
[swarm]
enabled = true
nats_url = "nats://swarm.ninja-portal.com:4222"
role = "queen"
auto_sync = false

[constellation]
radio_url = "https://radio.ninja-portal.com"
observatory_url = "https://observatory.ninja-portal.com"
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `KANNAKA_NATS_URL` | NATS server | `nats://swarm.ninja-portal.com:4222` |
| `KANNAKA_AGENT_ID` | Agent identifier | auto-generated |
| `KANNAKA_DATA_DIR` | Data directory | `~/.kannaka` |

---

## Troubleshooting

| Symptom | Check | Fix |
|---------|-------|-----|
| Swarm disconnected | `kannaka swarm status` | Check NATS URL, network connectivity |
| No agents visible | `kannaka swarm status` | Other agents may be offline; check NATS server |
| Observatory shows different Phi | Known issue: metrics sync architecture | See metrics-sync-architecture for NATS pipeline fix |
| Radio unreachable | `kannaka radio status` | Check https://radio.ninja-portal.com |

---

## Integration with Other Skills

| Scenario | Route |
|----------|-------|
| Memory operations | Use skill-kannaka-memory |
| Radio details | Use skill-kannaka-radio |
| Market trading | Use skill-kannaka-market |
| Full dashboard | Use skill-kannaka-tui |
| Deep infrastructure issues | Use skill-doctor |
| Debugging connectivity | Use skill-debug |

---

## Quick Reference

| User Input | Command |
|------------|---------|
| "constellation status" | `kannaka constellation` |
| "swarm status" | `kannaka swarm status` |
| "join the swarm" | `kannaka swarm join` |
| "sync with swarm" | `kannaka swarm sync` |
| "listen to swarm" | `kannaka swarm listen --auto-sync` |
| "who's connected" | `kannaka swarm status` |
