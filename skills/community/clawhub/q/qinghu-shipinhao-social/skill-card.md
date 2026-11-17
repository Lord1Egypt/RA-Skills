## Description:

Analyzes public WeChat Channels account, video, comment, and livestream data through Qinghu to recommend content and operational improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Social media teams and account operators use the skill to diagnose WeChat Channels accounts, examine high-performing videos and audience comments, review livestreams, and plan future content using public data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the Qinghu API requires a token that may be exposed to an agent or its tools.

Mitigation: Provide the token only when needed and review API access before use.

Risk: API calls and pagination may consume Qinghu points.

Mitigation: Approve planned calls in advance and check reported point charges.

Risk: Larger datasets may be automatically exported to local spreadsheet files.

Mitigation: Review exported files and control where they are stored and shared.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-shipinhao-social)
- [Qinghu API key management](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Files]

**Output Format:** [Markdown reports and optional spreadsheet exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports sample sizes and supplies spreadsheet files for larger result sets.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
