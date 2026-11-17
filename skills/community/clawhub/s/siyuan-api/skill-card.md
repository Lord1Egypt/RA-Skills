## Description:

Local SiYuan API integration for notebook, document, block, asset, database/attribute view, and limited SQL operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xybio](https://clawhub.ai/user/xybio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to let an agent work with a local SiYuan workspace: managing notebooks, documents, blocks, assets, database rows, and limited read-oriented SQL queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify local SiYuan workspace content when the API token is available.

Mitigation: Install only when local workspace automation is intended, keep the API token in environment variables, and avoid logging or echoing the token.

Risk: Using a non-loopback HTTP LAN endpoint can expose the SiYuan API token or workspace operations on an untrusted network.

Mitigation: Prefer localhost or 127.0.0.1; for another LAN machine, use HTTPS or a trusted private network and rotate the token if exposure is suspected.

Risk: Broad file, SQL, proxy, or conversion operations could expand the impact beyond ordinary note management.

Mitigation: Stay within the curated safe API scope, prefer structured note APIs, keep SQL read-oriented and limited, and avoid proxy or external conversion endpoints.

## Reference(s):

- [SiYuan Safe API Reference](references/safe-api.md)
- [SiYuan Project](https://github.com/siyuan-note/siyuan)
- [ClawHub Skill Page](https://clawhub.ai/xybio/skills/siyuan-api)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with inline code blocks and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses environment-based SiYuan API configuration and local endpoint constraints.]

## Skill Version(s):

1.4.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
