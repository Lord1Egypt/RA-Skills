## Description:

Threshold Keel provides safety guardrails for autonomous agents by classifying actions, requiring structured approval before irreversible operations, and supporting optional CLI-backed audit trails and policy enforcement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andaltan](https://clawhub.ai/user/andaltan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add session-level safety gates for autonomous agents with access to files, messaging, email, browser, or APIs. It helps classify actions by risk tier, request structured approval, and optionally record auditable policy checks through the Keel CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill takes broad control over agent actions and may block or slow ordinary write operations.

Mitigation: Install it only when a session-wide safety gate is desired, and review expected workflows before relying on it.

Risk: The external CLI can log actions and sync activity to Threshold Cloud when KEEL_CLOUD_API_KEY is configured.

Mitigation: Prefer local-only use first, and set KEEL_CLOUD_API_KEY only when external storage of action logs is acceptable.

Risk: The skill depends on the separately installed threshold-keel package for durable policy checks and audit logging.

Mitigation: Verify the threshold-keel package source and version before installation, and treat instructions-only mode as behavioral guidance rather than a durable audit system.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andaltan/skills/threshold-keel)
- [Threshold Keel homepage](https://thresholdsignalworks.com/keel)
- [Threshold Cloud](https://thresholdsignalworks.com/cloud)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command snippets, risk classifications, and structured approval prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use the threshold-keel CLI for local policy checks, audit logging, quarantine status, and optional cloud sync when configured.]

## Skill Version(s):

0.2.7 (source: server release metadata; artifact frontmatter reports 0.2.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
