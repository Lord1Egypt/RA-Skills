## Description:

Retrieves structured public Xiaohongshu data for keyword search, note detail and comment lookup, and blogger post monitoring to support trend, competitor, KOL, and content research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, content creators, and analysts use this skill to retrieve public Xiaohongshu notes, comments, and blogger posts. Agents can use the returned data for trend summaries, competitor comparison, KOL screening, comment analysis, and content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, target URLs, fetched public content, and GUAIKEI_API_TOKEN to the Guaikei service.

Mitigation: Use it only when that external data sharing is acceptable, configure the token through the environment, and avoid pasting the token into prompts or shared logs.

Risk: The API token is sent in request URLs, which can make surrounding request records sensitive.

Mitigation: Treat command output, proxy records, terminal history, and diagnostic logs from runs as sensitive when troubleshooting or sharing results.

Risk: The skill automatically saves full fetched results locally, which may include research targets and scraped public content.

Mitigation: Protect the local logs directory and delete saved results when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-bloggertrack)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Skill README](readme.md)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Guaikei API service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON command output with concise Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and may save full fetched results to local logs.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact frontmatter/package report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
