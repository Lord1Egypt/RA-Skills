## Description:

Scrapes the public PTT web BBS at ptt.cc to fetch board lists, category trees, article lists, search results, article metadata, comments, push/boo/neutral counts, board-wide push totals, and essence-area listings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanookai](https://clawhub.ai/user/nanookai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and analyze public PTT boards, articles, comments, search results, and push-score statistics without a PTT login.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The article command can fetch arbitrary web URLs and may reach unintended internal or local services.

Mitigation: Run in an environment with limited network access and pass only ptt.cc article URLs or relative /bbs paths.

Risk: Untrusted text could influence which article URL is fetched.

Mitigation: Do not let untrusted scraped content or user-provided text select article URLs without review.

Risk: Long PTT threads can produce large raw comment outputs.

Mitigation: Request summaries or bounded comment ranges for long threads instead of fetching or displaying all comments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nanookai/skills/ptt-bbs)
- [ClawHub publisher profile](https://clawhub.ai/user/nanookai)
- [PTT public web interface](https://www.ptt.cc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON-producing script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bundled script outputs UTF-8 JSON; article and comment presentation may include raw public PTT text unless summarization is requested or copyrighted embedded material is present.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
