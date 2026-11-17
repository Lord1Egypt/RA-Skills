## Description:

Sage COO helps founders of 1-30 person teams turn company context, team operations, delivery workflows, decisions, and reviews into a practical operating cadence backed by local Sage company memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billzhuang6569](https://clawhub.ai/user/billzhuang6569)

### License/Terms of Use:

MIT-0

## Use Case:

Founders and small startup teams use this skill as an AI COO pair-working partner for company operating rhythm, team structure, workflows, delivery follow-up, decision records, and review cadence. It is intended for OpenClaw, Codex, and Claude Code workspaces that want persistent local company context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently modify workspace agent-instruction files.

Mitigation: Install it only in workspaces where Sage COO behavior is desired, and review managed identity blocks after initialization.

Risk: The skill stores company memory in local files under ~/.sage.

Mitigation: Avoid storing secrets or highly sensitive business data, and review privacy-sensitive entries before saving them.

Risk: The mirror feature can copy local Sage memory into a workspace folder.

Mitigation: Use the mirror only for browsing, and avoid creating it inside repositories or synced folders unless the copied content is intended to be shared.

## Reference(s):

- [Sage COO ClawHub release page](https://clawhub.ai/billzhuang6569/skills/sage-coo)
- [COO Identity](references/coo-identity.md)
- [COO Operating System](references/coo-operating-system.md)
- [COO Scenarios](references/coo-scenarios.md)
- [Sage DNA Protocol](references/sage-dna-protocol.md)
- [Write Routing](references/write-routing.md)
- [OpenClaw Workspace Bootstrap](references/openclaw-workspace-bootstrap.md)
- [Onboarding](references/onboarding.md)
- [Review Cadence](references/review-cadence.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update workspace identity files, initialize local Sage company memory under ~/.sage, and create a sage-mirror workspace copy for browsing.]

## Skill Version(s):

3.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
