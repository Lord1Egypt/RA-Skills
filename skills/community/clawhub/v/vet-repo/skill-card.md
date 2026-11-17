## Description:

Scan repository agent configuration files for known malicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itsnishi](https://clawhub.ai/user/itsnishi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use Vet Repo to scan unfamiliar or recently changed repositories for risky agent configuration patterns before trusting local agent settings, MCP configuration, or skill files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local agent-related project configuration, including MCP configuration files that may contain server details or inline secrets.

Mitigation: Run it only in repositories you are authorized to inspect and avoid sharing reports that expose sensitive configuration values.

Risk: Regex-based scanner findings can include false positives or miss risks outside the known pattern set.

Mitigation: Review findings before acting on them and use the report as an advisory security signal rather than a deterministic enforcement layer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itsnishi/skills/vet-repo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain-text security report with severity-grouped findings and actionable recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are grouped by CRITICAL, HIGH, MEDIUM, LOW, and INFO; scanner results may include false positives.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
