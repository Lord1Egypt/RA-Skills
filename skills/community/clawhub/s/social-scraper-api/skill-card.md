## Description:

Access real-time public social media data from TikTok, Instagram, YouTube, Reddit, Twitter, Twitch, Snapchat, and Threads via EnsembleData's REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marktristy](https://clawhub.ai/user/marktristy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to call EnsembleData endpoints and SDKs for collecting public social media profiles, posts, comments, and engagement data for monitoring, research, and analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: EnsembleData tokens may be exposed through shared URLs, logs, screenshots, notebooks, or source code.

Mitigation: Use environment variables or secret storage, redact logs, avoid sharing tokenized URLs, rotate tokens after exposure, and pin SDK versions.

Risk: Collected public social-media data can include comments, profile details, contact fields, or business information subject to platform terms and privacy rules.

Mitigation: Limit collection to lawful public-data use cases, minimize stored data, review platform and privacy obligations, and apply access controls to exported datasets.

Risk: Bulk scraping and paginated endpoints can consume metered units quickly.

Mitigation: Cap pagination depth, monitor usage with the free account usage endpoints, and set operational limits before large collection jobs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marktristy/skills/social-scraper-api)
- [EnsembleData API Documentation](https://ensembledata.com/apis/docs)
- [EnsembleData Pricing](https://ensembledata.com/pricing)
- [EnsembleData Python SDK](https://github.com/EnsembleData/ensembledata-python)
- [EnsembleData Node.js SDK](https://github.com/EnsembleData/ensembledata-node)
- [Postman Collection](https://elements.getpostman.com/view/fork?collection=33901342-37bb76fa-5bc5-4342-94b5-3a6f884daabd)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown documentation with REST endpoint tables and Python, Node.js, and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes token handling guidance, endpoint costs, pagination notes, error codes, and account usage monitoring examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
