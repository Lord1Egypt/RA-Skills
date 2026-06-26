# Structured Multi-Agent Deliberation Framework

> Provides a structured multi-agent deliberation framework with role schemas (action/guardian/observer/critic), verification protocols, and stopping criteria. Activate when designing multi-agent systems for non-trivial deliberation, instrumenting agent debates against sycophancy, or seeking an evaluable alternative to free-form group prompting.

A Claude Skill for running multi-agent deliberation that produces *evaluable* output — claims with explicit lifecycles, verifications with cross-agent evidence, decisions that cite specific support, and stopping criteria that prevent both premature consensus and infinite loops.

## Install

### Claude Code

```bash
clawhub install structured-deliberation
```

Or manually clone:

```bash
git clone https://github.com/<org>/structured-deliberation.git ~/.claude/skills/structured-deliberation
```

### OpenClaw / Hermes / Cursor

Standard agentskills.io-compatible install per platform.

## Quickstart

Once installed, the skill activates when you describe a multi-agent deliberation problem. Example:

> **You**: I want to evaluate 3 candidate architectures for our agent system, but free-form discussion keeps converging too fast — I think we're sycophanting.
>
> **AI** (with skill): "Let's instrument it. The 4-role structure gives you adversarial pressure that free-form doesn't. Stage 1: what's the deliberation question — which architecture is most robust under load + adversarial conditions, or which is fastest to ship? Stage 2: who plays Critic in your team? Stage 3: ..."

The skill walks 5 stages (domain → role configuration → round template → run rounds → synthesis), producing a deliberation protocol calibrated to your specific evaluation question.

## What this skill does

Provides:

1. **4 role schemas** (Action / Guardian / Observer / Critic) — each contributes a perspective the others can't substitute
2. **4 cross-validation checks** per round — artifacts must contact each other, not be siloed
3. **Claims + verifications infrastructure** — disagreements become testable claims with status lifecycles
4. **6 goal-driven stopping criteria** — explicit signals for when to end the deliberation
5. **Stress test protocol** — forced agent absence reveals which roles are load-bearing
6. **8 failure modes catalog** — sycophancy, drift, claim inflation, verification bypass, etc.
7. **Reference scripts** — `claims-validator.py`, `stopping-detector.py`, `round-controller.py` skeleton

## When NOT to use

- Simple multi-agent task delegation (not deliberation)
- Single-LLM with chain-of-thought is sufficient (no real perspective diversity needed)
- LLM ensemble for accuracy (different problem; use voting / consensus methods)

## Files

```
structured-deliberation/
├── SKILL.md
├── README.md
├── LICENSE
├── references/
│   ├── role-schemas.md
│   ├── verification-protocol.md
│   ├── claims-infrastructure.md
│   ├── stopping-criteria.md
│   └── failure-modes.md
├── templates/
│   ├── role-prompt.md.tmpl
│   ├── round-template.md.tmpl
│   └── artifact-schemas/
│       ├── action.md.tmpl
│       ├── guardian.md.tmpl
│       ├── observer.md.tmpl
│       └── critic.md.tmpl
├── examples/
│   ├── condensed-deliberation.md
│   └── stress-test-walkthrough.md
└── scripts/
    ├── claims-validator.py
    ├── stopping-detector.py
    └── round-controller.py
```

## Background

This skill captures a methodology developed across multiple multi-agent deliberation experiments. The 4-role structure, 4 cross-validation checks, 6 stopping signals, and stress test patterns all emerged from calibration findings — they're not hypothetical.

The companion skill [multi-dim-eval-framework](https://github.com/<org>/multi-dim-eval-framework) provides MADEF (the evaluation framework for measuring deliberation quality). The two skills compose: this one produces structured deliberation; that one evaluates the deliberation's quality.

## Versioning

Following [SemVer](https://semver.org/).

- `0.1.0` initial release with 4 role schemas, 4 cross-validation checks, claims infra, 6 stop signals, 8 failure modes, 3 reference scripts, 2 examples

## License

MIT

## Contributing

Issues and PRs welcome. Particularly interested in:

- Cross-domain role instantiations (how the 4 roles map to your domain)
- Failure mode contributions (new failure modes you've observed in your deliberations)
- Round-controller integrations for specific LLM APIs (Anthropic / OpenAI / etc.)
- Worked examples in domains beyond architecture review
