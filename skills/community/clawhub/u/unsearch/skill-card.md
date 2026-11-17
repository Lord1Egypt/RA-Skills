## Description:

Search the web, scrape content, and conduct deep research using the UnSearch API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rakesh1002](https://clawhub.ai/user/rakesh1002)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agent builders use this skill to configure agents for real-time web search, URL content extraction, deep research, and fact verification through the UnSearch API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, fact-check claims, target URLs, and extracted page content are sent to UnSearch.

Mitigation: Use the skill only for data approved for third-party processing, avoid secrets and private or regulated content unless policy permits it, and enable the documented zero-retention header for sensitive-but-approved queries.

Risk: The UnSearch API key is a credential required by the skill.

Mitigation: Store UNSEARCH_API_KEY in an approved secret or environment manager and avoid committing it to skill files, prompts, or shared configuration.

Risk: Generated search, research, extraction, and verification results may be incomplete or misleading.

Mitigation: Review sources and verification summaries before relying on results in business, legal, medical, financial, or other high-impact workflows.

## Reference(s):

- [UnSearch Homepage](https://unsearch.dev)
- [UnSearch Documentation](https://docs.unsearch.dev)
- [UnSearch API Reference](https://docs.unsearch.dev/api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with bash, JSON, Python, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UNSEARCH_API_KEY and sends approved queries, URLs, claims, and extracted content to the UnSearch API.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
