## Description:

Agent vision for web pages: scene summaries, attention-ranked elements, annotated screenshots, and state diffing via SurfAgent's perception engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentossoftware](https://clawhub.ai/user/agentossoftware)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to perceive active web pages, rank visible interactive elements, annotate screenshots, and compare page state after browser actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be used on logged-in pages or pages containing sensitive personal, payment, authentication, or private-message data.

Mitigation: Use it only with sites and accounts you are authorized to automate, and avoid annotating or sharing pages that expose passwords, MFA codes, payment data, private messages, or personal records.

Risk: Annotated screenshots and perception summaries may capture sensitive page content.

Mitigation: Review outputs before sharing or storing them, and redact sensitive content when screenshots or legends are needed for collaboration.

Risk: Blocker and captcha workflows can conflict with site rules or legal permissions.

Mitigation: Treat captcha-solving and blocker automation as sensitive activity, and use them only where site rules and legal authorization permit.

Risk: The SurfAgent daemon token protects browser automation access.

Mitigation: Protect the daemon token and limit access to the local SurfAgent daemon.

## Reference(s):

- [SurfAgent Homepage](https://surfagent.app)
- [ClawHub Skill Page](https://clawhub.ai/agentossoftware/skills/surfagent-perception)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, API Calls, Guidance]

**Output Format:** [Markdown guidance with tool call parameters and structured perception outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scene summaries, ranked element references, spatial clusters, state tokens, diff summaries, and annotated screenshot legends.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
