## Description:

Research TikTok and Instagram Reels to identify standout posts, creators, hooks, formats, and competitor patterns using SearchTok's public-post data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mitchell2398](https://clawhub.ai/user/mitchell2398)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and businesses use this skill to research organic short-form video performance, compare accounts, and develop evidence-backed content ideas or recurring monitoring reports. It requires a SearchTok plan and access through its connector or CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned CLI commands can run a changed package version.

Mitigation: Prefer the SearchTok connector or a pinned, reviewed CLI installation over bare npx commands.

Risk: Connecting the service grants access to the user's SearchTok account and research context.

Mitigation: Connect only if you trust SearchTok and review the account access before authenticating.

Risk: Scheduled monitoring can repeat account access and use plan credits.

Mitigation: Review the scheduled prompt, accounts, frequency, and expected credit use before enabling it.

## Reference(s):

- [SearchTok homepage](https://searchtok.app)
- [SearchTok MCP connector](https://searchtok.app/mcp)
- [SearchTok skill release](https://clawhub.ai/mitchell2398/skills/searchtok)
- [What's working playbook](references/whats-working.md)
- [Content ideas playbook](references/content-ideas.md)
- [Competitor watch recipe](recipes/competitor-watch.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown research summaries, content ideas, and monitoring prompts with links to source posts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes post-derived metrics and quoted hooks when available; some workflows consume plan credits.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
