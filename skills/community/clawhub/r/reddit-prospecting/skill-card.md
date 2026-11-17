## Description:

Find buying-intent leads on Reddit via Brave Search, without a Reddit account or OAuth, then score posts and generate value-first comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[3rdbrain](https://clawhub.ai/user/3rdbrain)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, marketing, and developer relations users use this skill to find Reddit discussions with buying intent through Brave Search, score prospects, and draft value-first response structures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends configured search queries to Brave Search and requires a Brave Search API key.

Mitigation: Provide BRAVE_API_KEY only in trusted agent environments and avoid submitting confidential or sensitive prospecting queries.

Risk: Search result titles, snippets, and URLs are untrusted terminal output, and the security evidence notes terminal-output hygiene issues.

Mitigation: Treat displayed search results as untrusted, avoid copying terminal control characters, and prefer a sanitized release before using the output in automation.

Risk: The artifact includes local post-template and metrics helpers beyond the three commands described in SKILL.md.

Mitigation: Use the documented search, score, and comment commands unless the additional helpers are separately reviewed for the intended workflow.

Risk: Generated comment or engagement guidance could be used in ways that conflict with subreddit rules or disclosure expectations.

Mitigation: Review subreddit rules, disclose product affiliations when relevant, and keep comments value-first rather than promotional.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/3rdbrain/skills/reddit-prospecting)
- [Brave Search API](https://api.search.brave.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown-style structured guidance from Node.js CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BRAVE_API_KEY for search; score and comment helpers can run from provided arguments.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
