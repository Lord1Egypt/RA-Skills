## Description:

Extract posts from X (Twitter) timeline or profile pages with engagement metrics, media URLs, and download local copies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zyliu0](https://clawhub.ai/user/zyliu0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use xclaw to extract recent X timeline, profile, or search-result posts into local Markdown reports with engagement metrics, post URLs, and media references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may collect content from a logged-in X session and save post text, metrics, URLs, and downloaded media locally.

Mitigation: Use it only for content you are allowed to collect and archive, and review the saved ../../intel/x files before sharing or retaining them.

Risk: Local media downloads can store third-party content and increase local storage or privacy exposure.

Mitigation: Limit collection scope, remove unneeded media folders, and avoid archiving sensitive or unauthorized content.

## Reference(s):

- [xclaw Skill Page](https://clawhub.ai/zyliu0/skills/x-openclaw)
- [Publisher Profile](https://clawhub.ai/user/zyliu0)
- [X Home Timeline](https://x.com/home)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Analysis]

**Output Format:** [Markdown report with local media file references and inline shell/browser commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves reports under ../../intel/x and media under ../../intel/x/media/{YYYYMMDD}-{HHMMSS}.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
