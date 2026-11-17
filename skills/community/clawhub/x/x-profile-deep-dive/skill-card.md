## Description:

Analyzes X/Twitter profiles by collecting tweets, followings, and follower samples with tweety-ns, then generating Chinese-language profile dossiers with thematic classification, content style analysis, and network insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovensky1992-wk](https://clawhub.ai/user/lovensky1992-wk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw users use this skill to investigate a public X/Twitter account's recent content, posting patterns, audience signals, and social network. It is intended to produce a structured Chinese dossier for deciding whether and how to follow, reference, or further analyze the account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Twitter/X cookies with tweety-ns and a persisted session directory.

Mitigation: Use a dedicated low-privilege X account, keep cookie and session files private, and refresh or revoke cookies when no longer needed.

Risk: The tweety-ns dependency is unpinned in the release documentation.

Mitigation: Pin and review the dependency before deployment, then install it only in a controlled agent environment.

Risk: Generated reports may retain full tweets, profile details, and social-network information locally.

Mitigation: Store generated dossiers in an appropriate workspace, review them before sharing, and delete reports that contain sensitive or unnecessary personal data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lovensky1992-wk/skills/x-profile-deep-dive)
- [README](artifact/README.md)
- [Data Analysis Reference](artifact/references/data-analysis.md)
- [Report README Template](artifact/references/readme-template.md)
- [Network Template](artifact/references/network-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and JSON data produced from Python collection scripts and agent-authored analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a profile report directory with README.md, themed Markdown files, network.md, and intermediate JSON data.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
