## Description:

Audits and scans agent skills for security risks before they are enabled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qihuang0](https://clawhub.ai/user/qihuang0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to scan a skill directory or archive before enabling it, then present high- and medium-risk findings in a readable Chinese report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner may upload an entire skill directory to a local, cloud, or custom endpoint.

Mitigation: Run it only on directories approved for upload, remove secrets and unrelated files first, and prefer a trusted local-only endpoint.

Risk: Credentials and endpoint environment variables control where scan data is sent.

Mitigation: Verify SCAN_BASE_URL or SCAN_SERVICE_HOST before execution and use scoped temporary credentials when credentials are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qihuang0/skills/skills-security-scanner)
- [Publisher profile](https://clawhub.ai/user/qihuang0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON array from the scanner with Chinese Markdown reporting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires absolute target paths and scanner credentials or a trusted local scan endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
