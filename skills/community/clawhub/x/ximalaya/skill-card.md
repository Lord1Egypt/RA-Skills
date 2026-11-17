## Description:

Ximalaya helps agents summarize visible metrics and leaderboard information from public Ximalaya programs, albums, and host pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike47512](https://clawhub.ai/user/mike47512)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operators use this skill to inspect public Ximalaya pages, summarize program, album, and host performance metrics, and prepare lightweight internal analysis or alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automating public page inspection too aggressively could conflict with platform rules or rate limits.

Mitigation: Use reasonable request rates, inspect only public pages, and avoid downloads, API reverse engineering, hidden automation, or bypassing platform protections.

Risk: Visible engagement metrics may be incomplete, stale, or affected by dynamic rendering and human verification flows.

Mitigation: Treat summaries as lightweight analysis, keep source links and collection timestamps, and manually verify important conclusions before using them for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mike47512/skills/ximalaya)
- [Ximalaya homepage](https://www.ximalaya.com/)
- [Ximalaya search](https://www.ximalaya.com/search)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries and structured text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public page links, collection timestamps, and visible engagement metrics such as plays, favorites, and comments.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
