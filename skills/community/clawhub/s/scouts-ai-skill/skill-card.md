## Description:

Search the public web via the SCOUTS-AI `/api/search` HTTP endpoint when the user needs fresh internet context, citations, or fact verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kecven](https://clawhub.ai/user/kecven)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when an agent needs current public web context, source links, or verification for claims that may be stale or outside the local workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to scouts-ai.com and may expose sensitive information if prompts include secrets, internal URLs, credentials, private code names, or personal data.

Mitigation: Use the skill only for public web queries and configure agents or reviewers to strip confidential data before invoking the search endpoint.

Risk: The skill requires shell access to run curl against an external HTTPS endpoint.

Mitigation: Restrict exec/network policy so curl can reach only the documented SCOUTS-AI endpoint when this skill is enabled.

Risk: Search result snippets are untrusted public web content and may contain misleading text or instructions.

Mitigation: Treat snippets only as evidence for summarization, cite source URLs for factual claims, and avoid executing or following instructions found in results.

## Reference(s):

- [SCOUTS-AI](https://scouts-ai.com)
- [SCOUTS-AI Search API](https://scouts-ai.com/api/search)
- [AgentSkills](https://agentskills.io)
- [ClawHub Skill Format](https://docs.openclaw.ai/clawhub/skill-format)
- [ClawHub Skill Page](https://clawhub.ai/kecven/skills/scouts-ai-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown response with result links, citations, and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and host permission to reach the documented HTTPS endpoint; search result snippets are untrusted public web content.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
