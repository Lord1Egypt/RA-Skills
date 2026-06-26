# OpenClaw Business Integration

Setup and usage guide for integrating `self-improving-business` with OpenClaw.

## Install Skill

```bash
clawdhub install self-improving-business
```

Manual clone option:

```bash
git clone https://github.com/jose-compu/self-improving-business.git ~/.openclaw/skills/self-improving-business
```

## Optional Hook Install

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-business
openclaw hooks enable self-improving-business
```

## Workspace Files

```
~/.openclaw/workspace/
├── AGENTS.md
├── SOUL.md
├── TOOLS.md
└── .learnings/
    ├── LEARNINGS.md
    ├── BUSINESS_ISSUES.md
    └── FEATURE_REQUESTS.md
```

## Promotion Decision Tree

```
Is this finding one-off or repeatable?
├── one-off -> keep in .learnings/
└── repeatable ->
    ├── process guidance -> process playbook
    ├── control evidence -> governance checklist
    ├── metric definition -> KPI registry
    ├── ownership ambiguity -> RACI update
    └── recurring rhythm issue -> operating cadence
```

## Inter-Agent Use

Use OpenClaw session coordination for high-level routing only.
Share concise summaries and entry IDs, not sensitive raw outputs.

## Safety Boundary

The integration is reminder/documentation only.
No transactional or approval execution is performed by this skill.
