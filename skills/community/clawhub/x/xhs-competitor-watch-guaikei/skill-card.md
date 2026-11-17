## Description:

This command skill helps agents collect public Xiaohongshu content, note details, comments, and creator posts for competitor monitoring, trend research, KOL screening, and content planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, brand marketers, market analysts, and operations teams use this skill to search Xiaohongshu public content, inspect post details and comments, and monitor creator or competitor posting patterns. It supports public-data research workflows such as topic discovery, comment insight, KOL screening, competitive monitoring, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, links, and token-backed requests to guaikei.com.

Mitigation: Use it only when third-party processing is acceptable, avoid sharing GUAIKEI_API_TOKEN in chats or shared logs, and rotate the token if exposure is possible.

Risk: The skill saves unredacted result data locally under a logs directory.

Mitigation: Run it in a trusted workspace, avoid shared or CI environments for sensitive research, and periodically delete generated logs.

Risk: The skill is intended for public Xiaohongshu data and may be misused for unsupported private, hidden, or login-gated content requests.

Mitigation: Restrict use to public data, refuse private or login-state requests, and confirm that downstream use complies with authorization and distribution limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-competitor-watch-guaikei)
- [Guaikei API token site](https://www.guaikei.com)
- [Options and invocation guide](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON, files]

**Output Format:** [JSON status objects and saved JSON log files, with optional Markdown or text summaries prepared by the calling agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN; commands return success, empty, or error status with request metadata and results.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
