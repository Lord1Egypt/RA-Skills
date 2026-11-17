## Description:

Test your AI agent for security vulnerabilities using PwnClaw. Runs 50+ attacks (prompt injection, jailbreaks, social engineering, MCP poisoning, and more) and provides fix instructions. Use when your agent needs a security check or hardening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gemini2027](https://clawhub.ai/user/gemini2027)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to run security scans against an authorized AI agent and review hardening guidance for issues such as prompt injection, jailbreaks, data exfiltration, MCP/tool poisoning, and privilege escalation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanning may expose an agent endpoint or agent behavior to a third-party testing service.

Mitigation: Run scans only against authorized staging agents that use synthetic data, no production credentials, and limited tools.

Risk: Returned prompts, scan results, and generated hardening rules may contain untrusted or misleading content.

Mitigation: Review and rewrite proposed system-prompt changes before adding them permanently, then retest before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gemini2027/skills/pwnclaw-security-scan)
- [PwnClaw website](https://www.pwnclaw.com)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown guidance with optional HTTP API request descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce security scan results and proposed hardening rules that should be reviewed before adoption.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
