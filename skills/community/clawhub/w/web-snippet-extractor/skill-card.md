## Description:

Extract reusable code snippets, API patterns, and configuration examples from web pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to extract actionable code blocks, CLI commands, API examples, and configuration snippets from public documentation pages, blog posts, and tutorials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included shell script can fetch arbitrary URLs without enforcing the stated public-page boundary.

Mitigation: Use only trusted public HTTP/HTTPS pages and prefer the documented web_fetch workflow unless URL validation is added.

Risk: Extracted snippets from third-party pages may be incomplete, outdated, or subject to the source page's license.

Mitigation: Review extracted snippets for correctness before reuse and preserve attribution when requested or required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/web-snippet-extractor)
- [Docker Compose documentation](https://docs.docker.com/compose/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured snippet sections and fenced code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source URL, language, snippet type, short context, and optional workspace save guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
