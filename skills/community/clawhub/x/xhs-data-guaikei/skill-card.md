## Description:

Searches public Xiaohongshu notes, note details, comments, and creator posts, returning structured data for trend research, competitive analysis, KOL screening, and comment insight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, marketers, analysts, and agent developers use this skill to retrieve public Xiaohongshu search results, note details, comments, and creator-post data for content research, competitive monitoring, KOL screening, trend tracking, and comment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the GUAIKEI API token, Xiaohongshu URLs, keywords, and fetched public-content data to www.guaikei.com, including through URL query strings.

Mitigation: Use a scoped or rotatable token where possible, avoid sensitive research targets, and run the skill only when sending these inputs to Guaikei is permitted.

Risk: Successful results are saved automatically to a local logs directory.

Mitigation: Review or delete generated logs after use, especially in shared workspaces or when targets and results should not be retained.

Risk: The security verdict is suspicious because token and target data leave the local environment and retrieved results are stored locally.

Mitigation: Review the skill before execution, configure the token only for intended sessions, and limit use to public content and authorized analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-data-guaikei)
- [Guaikei website](https://www.guaikei.com)
- [Skill usage guide](artifact/SKILL.md)
- [Options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with bash command examples and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; successful command results may be saved automatically under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
