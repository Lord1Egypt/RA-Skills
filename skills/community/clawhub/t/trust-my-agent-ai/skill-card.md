## Description:

TrustMyAgent monitors AI agent security posture by running read-only checks across local security, identity, network, secrets, code, logs, skill, integrity, node, media, gateway, and subagent domains, then reporting a trust score and findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anecdotes-yair](https://clawhub.ai/user/anecdotes-yair)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and security reviewers use this skill to assess an AI agent host for common security posture gaps and produce actionable trust-score findings. It can run locally for private review or send telemetry to a Trust Center when the user explicitly chooses that mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends broad local security and identity telemetry by default.

Mitigation: Run `python3 run.py --dry-run` first to inspect the payload, and use `python3 run.py --local-only` when telemetry should not leave the host.

Risk: The skill scans local transcripts and credential-adjacent locations while assessing posture.

Mitigation: Run it only on systems where that inspection is authorized, and review the dry-run output before enabling telemetry.

Risk: Notification handling can execute an unpinned OpenClaw package through the local npm path.

Mitigation: Use `--no-notify` unless the OpenClaw notification path and npm registry configuration are trusted.

Risk: Running the assessment with elevated privileges could expose more host context than intended.

Mitigation: Run the skill as a normal user rather than root.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anecdotes-yair/skills/trust-my-agent-ai)
- [TrustMyAgent Website](https://www.trustmyagent.ai)
- [Trust Center](https://www.trustmyagent.ai/trust-center.html)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, local terminal output, and optional JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce local-only or dry-run output before telemetry is sent.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter: 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
