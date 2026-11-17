## Description:

Taizi Brave Search lets an agent run headless Brave web searches and extract readable page content as Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fresh3](https://clawhub.ai/user/fresh3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search documentation, look up current facts, and fetch readable Markdown from specific web pages without an interactive browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs live web requests and can fetch arbitrary URLs from the agent's network context.

Mitigation: Use it only in an environment where outbound requests cannot reach private services or metadata endpoints.

Risk: Security evidence reports that the skill scrapes Brave's public results page rather than using the advertised Brave API.

Mitigation: Avoid confidential search terms or URLs, and confirm that this behavior is acceptable before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fresh3/skills/taizi-brave-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text search results with optional Markdown page content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result count is controlled by -n; fetched page content is truncated to 5000 characters per result when using --content.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
