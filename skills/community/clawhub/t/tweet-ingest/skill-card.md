## Description:

Read Twitter/X content from a single tweet, thread, or user profile URL via TwitterAPI.io when an agent needs the content without browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch Twitter/X tweet, thread, or profile content from a URL and return markdown suitable for summarization, analysis, or RAG indexing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is not self-contained and references scripts that are not included in the artifact.

Mitigation: Install only after auditing the referenced tweet-ingest.py and rag_index.py scripts and confirming they match the documented behavior.

Risk: Twitter/X URLs and request data may be sent to external services, and the skill may rely on service credentials.

Mitigation: Use controlled credentials and review outbound data handling for TwitterAPI.io, Jina AI, Apify, and 1Password before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nissan/skills/tweet-ingest)
- [Publisher Profile](https://clawhub.ai/user/nissan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs clean markdown to stdout; errors are documented as markdown responses.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
