## Description:

XHS Competitor Watch helps agents retrieve Xiaohongshu public content by keyword, note URL, or creator profile URL for competitor monitoring, trend research, comment analysis, and report preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, content operators, and analysts use this skill to collect structured Xiaohongshu public note, comment, and creator-post data for competitor tracking, content planning, KOL screening, and trend reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Service tokens, keywords, and target Xiaohongshu URLs are sent to www.guaikei.com.

Mitigation: Use a dedicated low-privilege Guaikei token, avoid unnecessary xsec_token query parameters, and confirm that the research targets are appropriate for third-party processing.

Risk: Full command outputs are stored locally in the logs directory.

Mitigation: Delete or protect local logs when outputs include sensitive research targets, comments, creator URLs, or competitive analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-competitor-watch)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON command results with concise text or Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; outputs may include Xiaohongshu URLs, interaction metrics, comments, creator posts, and local log files.]

## Skill Version(s):

1.0.0 (source: server evidence, package.json, frontmatter metadata, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
