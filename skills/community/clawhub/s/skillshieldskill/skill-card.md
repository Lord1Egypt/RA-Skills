## Description:

AI Agent Skill Security Scanner - Detect malicious skills, verify signatures, analyze permissions, and provide trust ratings for the agent ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uexo](https://clawhub.ai/user/uexo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to scan agent skills for suspicious behaviors, permissions, credential-access patterns, networking, and signature status before installation or release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes a Moltbook publishing script with a hardcoded bearer token.

Mitigation: Remove the embedded token, rotate any exposed credential, and require an explicitly scoped credential supplied by the operator.

Risk: The skill presents A-F trust ratings that may be mistaken for proof that another skill is safe.

Mitigation: Treat scanner output as advisory and require human review of source, permissions, and provenance before installation or release.

Risk: Installation instructions include an unpinned package path.

Mitigation: Pin the intended version or source and compare server-provided hashes before running or distributing the skill.

Risk: Moltbook integration can make authenticated external API requests.

Mitigation: Run the integration only in an environment with approved network access and least-privilege credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uexo/skills/skillshieldskill)
- [Publisher profile](https://clawhub.ai/user/uexo)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or JSON security report with command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include trust ratings, warnings, permissions, hashes, summaries, and recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
