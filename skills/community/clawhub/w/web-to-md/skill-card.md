## Description:

Extracts readable markdown from user-provided URLs via a deterministic fallback chain (markdown.new -> r.jina.ai).

This skill is ready for commercial/non-commercial use.

## Publisher:

[chdlc](https://clawhub.ai/user/chdlc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to extract, summarize, or analyze content from specific user-provided URLs while preserving a clear extraction provenance label.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied URL text may be unsafe when copied into shell command examples.

Mitigation: Quote URLs, avoid shell-string interpolation, and review commands before execution.

Risk: Complete supplied URLs are forwarded to markdown.new or r.jina.ai.

Mitigation: Do not use the skill for private intranet pages, localhost URLs, signed links, invite or password-reset links, or URLs containing access tokens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chdlc/skills/web-to-md)
- [markdown.new extraction endpoint](https://markdown.new/{URL}?method=ai)
- [r.jina.ai browser extraction endpoint](https://r.jina.ai/{URL})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell command examples and source provenance labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and sends supplied URLs to external extraction services before falling back to agent tools.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
