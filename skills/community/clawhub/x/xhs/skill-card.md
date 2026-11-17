## Description:

XHS helps an agent draft, save, publish, manage, and review Xiaohongshu (RED) Creator Center posts through browser automation, with final publishing gated on explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mebusw](https://clawhub.ai/user/mebusw)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, studios, and agencies use this skill to prepare Xiaohongshu notes, upload images, save drafts or publish confirmed posts, reply to comments or DMs, and inspect visible Creator Center metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a logged-in Xiaohongshu Creator Center session, upload selected images, read visible account metrics, and draft or send social replies.

Mitigation: Install only when that level of account access is acceptable, and review content before confirming any publish or reply action.

Risk: Publishing or replying can create public-facing social content from a personal, team, studio, or agency account.

Mitigation: Require explicit user confirmation before publishing and treat ambiguous publish requests as draft-only.

Risk: Browser automation depends on the visible Creator Center session and can be blocked by login, verification, risk controls, or UI changes.

Mitigation: Pause for user login or verification, do not bypass captchas, SMS checks, or platform risk controls, and report manual steps when controls are unavailable.

## Reference(s):

- [XHS Skill on ClawHub](https://clawhub.ai/mebusw/skills/xhs)
- [Xiaohongshu Creator Center](https://creator.xiaohongshu.com)
- [Xiaohongshu Creator Center Publish Page](https://creator.xiaohongshu.com/publish/publish?from=menu&target=image)
- [Post Templates](references/post-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with structured action/status fields and inline commands when file staging is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account, title, mode, status, inserted topic-chip count, formatted tags, draft-save state, and next steps.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
