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
mkdir -p .openclaw/hooks
cp -r hooks/openclaw .openclaw/hooks/self-improving-business
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

## Scope

This skill does not read other sessions, send cross-session messages, spawn background agents, or read other installed skills. Log redacted notes in this workspace only.

## Safety Boundary

The integration is reminder/documentation only.
No transactional or approval execution is performed by this skill.
