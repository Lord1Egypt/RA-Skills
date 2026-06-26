# OpenClaw Integration

Complete setup and usage guide for `self-improving-negotiation` in OpenClaw.

Repository:
- `https://github.com/jose-compu/self-improving-negotiation.git`

## Workspace Structure

```text
~/.openclaw/
├── workspace/
│   ├── AGENTS.md
│   ├── SOUL.md
│   ├── TOOLS.md
│   ├── MEMORY.md
│   └── .learnings/
│       ├── LEARNINGS.md
│       ├── NEGOTIATION_ISSUES.md
│       └── FEATURE_REQUESTS.md
├── skills/
│   └── self-improving-negotiation/
└── hooks/
    └── self-improving-negotiation/
```

## Install

```bash
clawdhub install self-improving-negotiation
```

Manual:

```bash
git clone https://github.com/jose-compu/self-improving-negotiation.git ~/.openclaw/skills/self-improving-negotiation
```

## Optional Hook

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-negotiation
openclaw hooks enable self-improving-negotiation
```

## Promotion Targets

Promote recurring learnings to:
- negotiation playbooks
- objection libraries
- concession guardrails
- BATNA checklists
- deal review templates

## Trigger Mapping

| Trigger | Log Type | Category |
|---------|----------|----------|
| Deadlock | `NEG` | `framing_miss` / `escalation_misalignment` |
| Repeated objections | `LRN` | `objection_handling_gap` |
| Concession leakage | `NEG` | `concession_leak` |
| BATNA undefined | `NEG` | `batna_weakness` |
| Term ambiguity | `NEG` | `agreement_risk` |
| Anchor drift | `LRN` | `anchor_error` |

## Safety Note

Skill and hooks are reminder-only and do not auto-accept terms or approvals.
