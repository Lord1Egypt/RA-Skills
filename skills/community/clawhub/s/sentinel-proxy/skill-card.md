## Description:

Sentinel-Proxy is an AI firewall for Open Claw agents that scrubs inbound prompts, tool inputs, and tool results for prompt injection, jailbreak, and data exfiltration attempts using Sentinel's detection pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c0ri](https://clawhub.ai/user/c0ri)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add Sentinel prompt and tool-result inspection hooks to Open Claw agents. It is intended to reduce prompt-injection, jailbreak, malicious tool-output, and data-exfiltration risk during agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt, tool argument, and tool result content is sent to a third-party Sentinel service for inspection.

Mitigation: Use the skill only where Sentinel's privacy and retention terms fit the data, and avoid regulated or secret-heavy workflows unless that review is complete.

Risk: The hook behavior can fail open when Sentinel is not configured or unreachable.

Mitigation: Use tightly controlled environments and define fail-closed behavior for sensitive workflows before relying on the skill for protection.

Risk: The Sentinel API key enables access to the inspection service.

Mitigation: Protect the key, scope its use to the intended agent environment, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/c0ri/skills/sentinel-proxy)
- [Project homepage](https://github.com/c0ri/sentinel-skills)
- [Sentinel AI Firewall](https://sentinelaifirewall.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON hook envelopes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hook scripts can pass, block, or rewrite prompt and tool-result content based on Sentinel responses.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
