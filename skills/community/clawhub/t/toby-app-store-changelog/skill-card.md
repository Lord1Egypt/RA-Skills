## Description:

Create user-facing App Store release notes by collecting and summarizing all user-impacting changes since the last git tag or a specified ref.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release managers use this skill to turn git history into concise, user-facing App Store release notes. It helps collect changes, filter for user impact, group updates, and draft clear storefront-ready bullets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper reads commit history and touched file names from repositories where it is used.

Mitigation: Use it only in repositories where sharing commit subjects and file paths with the agent is acceptable.

Risk: Manual ref arguments may be unsafe if copied from an untrusted source before validation and quoting are added.

Mitigation: Pass only trusted tag, branch, or commit refs when collecting release changes.

## Reference(s):

- [App Store Release Notes Guidelines](references/release-notes-guidelines.md)
- [Complete Setup Guide](https://skillboss.co/skill.md)
- [ClawHub Skill Page](https://clawhub.ai/tobeyrebecca/skills/toby-app-store-changelog)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown bullet lists with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [User-facing bullets should map to real changes and avoid internal-only work.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
