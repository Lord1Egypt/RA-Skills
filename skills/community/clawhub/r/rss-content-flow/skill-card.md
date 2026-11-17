## Description:

Rss Content Flow helps agents manage RSS subscriptions, fetch recent articles, filter stale or promotional items, and support AI-assisted content planning workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, marketers, and developers use this skill to monitor RSS feeds, collect recent article ideas, and prepare source material for AI-assisted platform-specific drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound requests to configured RSS URLs, including custom URLs added by a user.

Mitigation: Use trusted public RSS feeds only, avoid internal or sensitive URLs, and review feed configuration before execution.

Risk: RSS content may be untrusted, misleading, promotional, or adversarial even after basic filtering.

Mitigation: Treat fetched feed text as untrusted source material and review extracted titles, links, and summaries before reuse.

Risk: The release describes AI rewrite and publishing workflows that could save or publish generated content without enough confirmation.

Mitigation: Require explicit human approval before every external write, Feishu save, or social posting action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/rss-content-flow)
- [Publisher profile](https://clawhub.ai/user/freedompixels)
- [AISoBrand website](https://aisobrand.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and optional JSON article lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches configured RSS feeds, summarizes recent entries for review, and can provide source material for downstream drafting or publishing tools.]

## Skill Version(s):

1.2.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
