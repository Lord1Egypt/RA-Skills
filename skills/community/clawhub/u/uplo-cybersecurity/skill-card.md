## Description:

AI-powered cybersecurity knowledge management. Search threat intelligence, vulnerability assessments, incident response plans, and compliance documentation with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Security teams use this skill to search and synthesize threat intelligence, vulnerability assessments, incident response plans, security policies, and compliance evidence from a UPLO-backed organizational knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a mutable MCP package and a secret API token.

Mitigation: Use a dedicated least-privilege UPLO token, pin or otherwise control the MCP package version, and run the server in a constrained environment.

Risk: The skill can expose broad organizational cybersecurity context through exports, incident logs, and knowledge searches.

Mitigation: Require users to confirm and sanitize full organizational exports or incident logs, and enforce the configured clearance and classification tiers.

## Reference(s):

- [ClawHub listing: Uplo Cybersecurity](https://clawhub.ai/roojenkins/skills/uplo-cybersecurity)
- [Publisher profile: roojenkins](https://clawhub.ai/user/roojenkins)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline tool calls, shell commands, and JSON configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a UPLO instance URL and API key; responses should respect configured classification tiers.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
