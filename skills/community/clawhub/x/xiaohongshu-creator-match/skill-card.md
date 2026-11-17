## Description:

Filters Xiaohongshu creator candidates by keywords, engagement signals, public post performance, creator activity, note details, and comments so an agent can support creator matching, market research, topic selection, competitor monitoring, and sentiment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

External operators, creators, marketing analysts, and agent users use this skill to retrieve public Xiaohongshu search results, note details, creator post lists, and comments for creator screening, campaign planning, trend analysis, and competitive monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, Xiaohongshu URLs, and GUAIKEI_API_TOKEN are sent to guaikei.com.

Mitigation: Use only approved public-data workflows, provide a scoped token where possible, and avoid submitting private or sensitive material.

Risk: Returned public-content results may be retained in local logs and can include creator or commenter information.

Mitigation: Review and delete retained logs when they are no longer needed, and restrict sharing of exports that contain personal comments or creator data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/xiaohongshu-creator-match)
- [Project homepage listed by ClawHub metadata](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [Options reference](references/options.md)
- [Troubleshooting reference](references/troubleshooting.md)
- [Changelog](references/changelog.md)
- [Token setup page](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON result summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN; command results may be stored in local logs.]

## Skill Version(s):

1.1.4 (source: server release metadata, SKILL.md frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
