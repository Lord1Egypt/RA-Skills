## Description:

Yidun Skill Sec scans third-party code packages with local behavioral analysis and default-on cloud threat intelligence to produce a security verdict before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yd-dev](https://clawhub.ai/user/yd-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to vet third-party agent skills or code packages before installation. It helps decide whether to install, block, or require review based on file fingerprints, behavioral indicators, cloud intelligence, and a scored verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends package metadata and matched code lines to a third-party cloud service by default.

Mitigation: Use YIDUN_SKILL_SEC_CLOUD=false for private, proprietary, or customer code when remote analysis is not acceptable.

Risk: Redaction may not remove every sensitive value from snippets selected for cloud analysis.

Mitigation: Enable YIDUN_SKILL_SEC_LOG_PAYLOAD=true and review the redacted payload before allowing cloud analysis.

Risk: The server security verdict is suspicious because the privacy claims are broader than the observed risk supports.

Mitigation: Require a human review of cloud transmission behavior and privacy language before approving deployment in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yd-dev/skills/yidun-skill-sec)
- [Publisher profile](https://clawhub.ai/user/yd-dev)
- [ClawHub homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces security scores, behavior labels, verdicts, and installation guidance.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
