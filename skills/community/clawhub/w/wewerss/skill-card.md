## Description:

WeWeRSS helps agents subscribe to WeChat public accounts and RSS sources through the Open Channel API, then retrieve raw article content for daily digest workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eggyrooch-blip](https://clawhub.ai/user/eggyrooch-blip)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage WeWeRSS channels, add or remove feed sources, retrieve raw articles, and expose an Atom feed for downstream agent summarization or digest workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using an untrusted WeWeRSS instance or submitting confidential source URLs can expose sensitive feed data to an unauthorized server.

Mitigation: Use a trusted HTTPS, self-hosted, or organization-controlled WeWeRSS instance for sensitive workflows, and submit only sources that server is authorized to fetch and store.

Risk: Running the delete command with the wrong source identifier can remove an intended subscription.

Mitigation: List sources first and verify SOURCE_ID before issuing the delete request.

## Reference(s):

- [WeWeRSS ClawHub Skill](https://clawhub.ai/eggyrooch-blip/skills/wewerss)
- [WeWeRSS Homepage](https://github.com/punkpeye/wewerss)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples and API response field descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; API responses contain raw article metadata, raw text when available, and Atom XML, with no AI-generated summaries, tags, categories, or scores.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
