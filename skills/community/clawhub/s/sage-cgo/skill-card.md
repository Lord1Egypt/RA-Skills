## Description:

Sage CGO helps 1-30 person startup teams build a focused growth system across audience, channels, content, experiments, and monetization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billzhuang6569](https://clawhub.ai/user/billzhuang6569)

### License/Terms of Use:

MIT-0

## Use Case:

External founders and small startup teams use this skill as an AI growth partner to choose focused channels, define audiences, plan content systems, design growth experiments, and record confirmed growth decisions. It is intended for growth strategy and operating-system guidance rather than black-hat growth tactics or unreviewed performance claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent workspace instruction changes can influence future agent behavior after installation.

Mitigation: Install only in workspaces where Sage CGO should persist, and review generated AGENTS.md, CLAUDE.md, and related files before continuing.

Risk: Company memory copied into a workspace mirror can expose private business context.

Mitigation: Avoid creating sage-mirror inside a Git repo, cloud-synced folder, or shared workspace unless that exposure is acceptable.

Risk: Sensitive company facts can persist in the local Sage memory directory.

Mitigation: Keep sensitive company facts out of ~/.sage and review stored growth memory before sharing or syncing the environment.

## Reference(s):

- [Sage CGO ClawHub skill page](https://clawhub.ai/billzhuang6569/skills/sage-cgo)
- [Sage CGO Identity](references/cgo-identity.md)
- [CGO Growth Operating System](references/cgo-growth-operating-system.md)
- [CGO Scenarios](references/cgo-scenarios.md)
- [Chinese Social Media Platform Knowledge Base](references/platforms.md)
- [Sage CGO and Company DNA](references/sage-dna-protocol.md)
- [CGO Write Routing](references/write-routing.md)
- [CGO Onboarding](references/onboarding.md)
- [CGO Review Cadence](references/review-cadence.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional shell commands and file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initialize or update ~/.sage growth memory and workspace identity files when invoked by the user.]

## Skill Version(s):

3.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
