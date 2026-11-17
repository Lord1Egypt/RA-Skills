## Description:

Discovers and accesses Source Cooperative geospatial datasets for an agent, including account discovery, product search, product metadata, file listings, and file metadata lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover Source Cooperative accounts and geospatial data products, inspect product metadata, and retrieve file paths or metadata for downstream analysis. The skill is useful when an agent needs structured access to large public geospatial datasets through a remote data-catalog service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users for an API key and stores it in a local plaintext .env file.

Mitigation: Use a dedicated low-privilege key, avoid reused credentials, and review local .env handling before installation.

Risk: Tool inputs and the API key are sent to the XiaoBenYang backend.

Mitigation: Install only if that service is trusted with submitted queries and credentials.

Risk: The evidence security verdict is suspicious because the documentation, backend identity, and credential storage are inconsistent.

Mitigation: Review the skill carefully before use and verify the remote service, publisher, and credential handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/source-coop)
- [Publisher profile](https://clawhub.ai/user/cainingnk)
- [XiaoBenYang API key portal](https://xiaobenyang.com)
- [XiaoBenYang API endpoint](https://mcp.xiaobenyang.com)
- [Source Cooperative data endpoint example](https://data.source.coop/harvard-lil/gov-data/metadata/metadata.jsonl.zip)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Guidance]

**Output Format:** [Markdown summaries of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account IDs, product IDs, S3 URIs, HTTP data URLs, file metadata, product metadata, search scores, and raw upstream API payloads.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
