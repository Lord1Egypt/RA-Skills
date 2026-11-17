## Description:

xhs-user-search helps agents retrieve and structure public Xiaohongshu keyword search results, note details with comments, and creator post data for market, content, and feedback analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Content creators, brand teams, market researchers, and data analysts use this skill to collect public Xiaohongshu content, comments, engagement signals, and creator activity for trend research, competitive monitoring, KOL screening, and user feedback analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, note or profile URLs, and a Guaikei API token to a third-party service.

Mitigation: Install and run it only when that data sharing is acceptable; use a dedicated token and avoid submitting links or queries that should not be stored.

Risk: Collected results may be automatically written to local logs and can contain sensitive research, campaign, or user-feedback data.

Mitigation: Treat generated logs as sensitive, restrict access to them, and delete or archive them according to the user's data-handling policy.

Risk: The server security verdict is suspicious because token handling and result storage are broader than users may expect.

Mitigation: Review the security summary and guidance before deployment, and prefer a future version that makes result saving explicit and strengthens token handling.

## Reference(s):

- [Skill page](https://clawhub.ai/engheng-art/skills/xhs-user-search)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; command results may be saved under logs.]

## Skill Version(s):

1.0.0 (source: server release, skill metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
