## Description:

Publish HTML, Markdown, text, PDF, Word, and PowerPoint content as ShareOne links, and manage existing shares, comments, and settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beep879](https://clawhub.ai/user/beep879)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI agents use this skill to publish web pages and documents to ShareOne for sharing, then update or manage those shares, retrieve content, and work with comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous sharing requests may lead to publishing conversation content without a clear provider or audience, and the scanner reports missing sensitive-content checks.

Mitigation: Use the skill only when ShareOne is explicitly selected, and review the content and intended audience before publishing.

Risk: The security guidance reports a share deletion confirmation gap.

Mitigation: Confirm the target share and deletion action before deleting it.

Risk: Scanner coverage was partial, so reported concerns may not cover every behavior.

Mitigation: Review the skill and its requested actions before installation and use.

## Reference(s):

- [ShareOne skill on ClawHub](https://clawhub.ai/beep879/skills/shareone)
- [ShareOne website](https://shareone.vip)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Files]

**Output Format:** [Share links, downloaded content or files, and operation results in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May publish content to a public link; ShareOne access settings such as passwords and watermarks can be applied.]

## Skill Version(s):

1.12.0 (source: SKILL.md metadata, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
