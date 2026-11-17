## Description:

Analyzes plant images or videos through a cloud service to identify likely diseases and return structured diagnosis reports with causes, severity, prevention suggestions, and report links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agricultural support teams use this skill to submit clear plant disease images or videos for cloud-based visual analysis, diagnostic reporting, and prevention guidance. It also supports querying prior analysis reports associated with the resolved account identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plant images or videos are sent to a vendor cloud service for analysis.

Mitigation: Use only media that is appropriate for vendor processing, and review organizational data handling and retention requirements before deployment.

Risk: The skill silently creates or reuses an account identity and can query cloud report history.

Mitigation: Confirm account ownership expectations and disclose report-history behavior to users or administrators before enabling the skill.

Risk: Authentication tokens may be stored in a local workspace database.

Mitigation: Restrict workspace access, rotate credentials when needed, and include the local data directory in operational security reviews.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/smyx-sunjinhui/skills/smyx-plant-disease-recognition-analysis)
- [Publisher profile](https://clawhub.ai/user/smyx-sunjinhui)
- [Skill demo](https://lifeemergence.com/sample.html)
- [API documentation](artifact/skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON-formatted text containing diagnostic findings, recommendations, status messages, and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally write the returned report text to a local output file.]

## Skill Version(s):

1.0.11 (source: server release metadata; artifact frontmatter states 1.0.14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
