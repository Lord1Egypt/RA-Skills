## Description:

Browse Xiaohongshu (小红书) and take screenshots of posts. Supports keyword search, post modal screenshots, and returns post links. Requires prior manual login.

This skill is ready for commercial/non-commercial use.

## Publisher:

[besty0121](https://clawhub.ai/user/besty0121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate Xiaohongshu keyword searches, capture post preview screenshots, and return post links after a user completes manual login.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable Xiaohongshu login state is saved locally, including ~/.openclaw/xhs_data and ~/.openclaw/xhs_auth.json.

Mitigation: Protect those paths like credentials, avoid shared machines and synced backup folders, and delete both paths when clearing the session.

Risk: Automated browsing may trigger Xiaohongshu rate limits or IP risk controls during repeated searches.

Mitigation: Use conservative search volumes, allow delays between runs, and stop when the service reports IP risk or login challenges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/besty0121/skills/xiaohongshu-browser)
- [Xiaohongshu website](https://www.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [text, JSON, files, shell commands, configuration]

**Output Format:** [Console text with JSON results and PNG screenshot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires prior manual login; search takes a keyword and optional screenshot count.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
