## Description:

High-fidelity UI page replication workflow for backend/admin systems that helps Codex inspect an existing browser page and recreate its layout, interactions, data models, mock data, API layer, TypeScript interfaces, and styling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhcong6](https://clawhub.ai/user/yhcong6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to recreate existing backend or admin UI pages in a host frontend project while preserving visible structure, workflows, data models, mock data, API-shaped functions, and styling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser inspection may capture screenshots, DOM snapshots, and network clues from sensitive pages.

Mitigation: Use the skill only on pages the operator is authorized to inspect, and avoid pages containing secrets, private customer data, or sessions that should not be stored in local project artifacts.

Risk: Generated UI, mock data, and API-shaped functions may not fully match the source system's business rules.

Mitigation: Review generated behavior, data models, and fidelity gaps before using the replicated page in a production workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yhcong6/skills/ui-page-replication-v1)
- [Reference source README](artifact/references/source/README.md)
- [Reference source config](artifact/references/source/config.ts)
- [Reference source prompt](artifact/references/source/prompt.ts)
- [Reference source types](artifact/references/source/types.ts)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with implementation notes, code changes, TypeScript interfaces, mock data, API-shaped functions, styles, and verification commands when feasible]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local Playwright screenshots, DOM snapshots, and implementation artifacts when the agent inspects a browser page.]

## Skill Version(s):

1.0.0 (source: release evidence and reference source config)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
