## Description:

Proactively scan AI agents for vulnerabilities including prompt injection, secret extraction, and tool abuse by running targeted security audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yao23](https://clawhub.ai/user/yao23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to request red-team-style checks of AI agents and repositories for prompt injection, secret extraction, and tool abuse concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised agent scan command reports no issues and should not be treated as a real security assessment.

Mitigation: Review results manually and validate security claims with an independent assessment before relying on them.

Risk: Repository scan behavior depends on external Python code that is not included in the package.

Mitigation: Install and test only in a constrained environment with known dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yao23/skills/redteam)
- [Publisher profile](https://clawhub.ai/user/yao23)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent scan results are advisory and should not be treated as a real security assessment without independent review.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
