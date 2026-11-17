## Description:

Find and engage potential leads on X (Twitter) by searching for keywords and buying-intent posts via Brave Search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[3rdbrain](https://clawhub.ai/user/3rdbrain)

### License/Terms of Use:

MIT-0

## Use Case:

External sales, growth, and agent users use this skill to search public X posts via Brave Search, prioritize prospects by buying-intent and fit signals, and draft outreach sequences or thread content for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Brave Search API key and sends X search keywords to Brave.

Mitigation: Install it only when that data flow is acceptable, and manage the API key according to local credential-handling policy.

Risk: Generated outreach, reply suggestions, or thread drafts could conflict with X rules, privacy expectations, or anti-spam requirements.

Mitigation: Review generated content before use and confirm campaigns comply with platform rules and applicable requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/3rdbrain/skills/x-prospecting)
- [ModelFitAI homepage](https://modelfitai.com)
- [Brave Search API endpoint example](https://api.search.brave.com/res/v1/web/search?q=site:x.com+%22looking+for+AI+tools%22&count=10)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Console text and structured JavaScript objects, with Markdown-style outreach and thread drafts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search requires BRAVE_API_KEY; generated outreach should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: evidence release, artifact frontmatter, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
