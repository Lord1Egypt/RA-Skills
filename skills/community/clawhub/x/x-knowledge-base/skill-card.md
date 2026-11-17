## Description:

Collects X bookmarks and converts them into an Obsidian knowledge base with AI summaries, wiki-style cross-links, and interest trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hidicence](https://clawhub.ai/user/hidicence)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn X bookmark activity into local Markdown notes, Obsidian-ready knowledge entries, AI-generated summaries, and trend reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles X session credentials and bookmark-derived data that may be private or work-sensitive.

Mitigation: Run it in a dedicated low-privilege environment, avoid running as root, and provide credentials only through environment variables.

Risk: Jina and MiniMax processing can expose URLs and article text outside the user's machine.

Mitigation: Review bookmark content before processing and use MiniMax only when external processing is acceptable for the data involved.

Risk: The skill writes and rewrites local bookmark and Obsidian note files with limited safeguards.

Mitigation: Keep backups of bookmark and vault directories and test on a small subset before running over an important vault.

Risk: A custom MiniMax endpoint could redirect sensitive text or credentials to an untrusted host.

Mitigation: Do not set MINIMAX_ENDPOINT to an untrusted host.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/hidicence/skills/x-knowledge-base)
- [Jina AI Reader service](https://r.jina.ai/)
- [MiniMax Anthropic-compatible messages endpoint](https://api.minimax.io/anthropic/v1/messages)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown notes, Obsidian wiki-links, JSON trend data, shell command output, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local bookmark, Obsidian, and trend files; optional AI summaries depend on configured external API credentials.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
