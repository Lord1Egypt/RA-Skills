## Description:

Searches public Xiaohongshu notes and creator posts, retrieves note details and comments, and returns engagement data for content research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, brands, and marketing teams use this skill to research public Xiaohongshu trends, compare creator posts, review engagement, and analyze note comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms or links and the API token are sent to a third-party service.

Mitigation: Use only when sharing those inputs with guaikei.com is acceptable; avoid private, login-only, or non-public content.

Risk: Returned results are saved in local temporary logs and may contain sensitive research targets or comments.

Mitigation: Protect access to the logs and delete them when no longer needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/xiaohongshu-note-search)
- [Skill homepage (listed in ClawHub metadata; import provenance unavailable)](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [API token and service information](https://www.guaikei.com)
- [Usage options](references/options.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries of JSON search results, note details, creator posts, or comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public content only; a configured GUAIKEI_API_TOKEN is required.]

## Skill Version(s):

1.1.4 (source: ClawHub release, frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
