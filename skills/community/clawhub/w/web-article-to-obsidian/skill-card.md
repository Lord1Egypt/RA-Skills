## Description:

Extracts public web articles, cleans the content, classifies it by industry, and saves raw text plus structured Markdown into an Obsidian knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to turn public article URLs from supported Chinese finance and social platforms, plus general webpages, into organized Obsidian notes. It is intended for article capture, cleanup, classification, and local knowledge-base storage workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs, including private or internal links if a user supplies them.

Mitigation: Use it only with public article URLs and review submitted URLs before running extraction.

Risk: Fallback extraction can send submitted URLs to Tavily or Firecrawl.

Mitigation: Avoid sensitive URLs, configure third-party API access intentionally, and prefer local extraction methods when URL disclosure is not acceptable.

Risk: Fetched content is persisted as raw text and structured Markdown in the configured Obsidian vault.

Mitigation: Configure the vault path deliberately, use dry-run mode for testing, and review stored copies as persistent local records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cgxxxxxxxxxxxx/skills/web-article-to-obsidian)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files, raw text archives, command examples, and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write persistent local records to the configured Obsidian vault and may use third-party extraction services during fallback.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter declares 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
