## Description:

Manage Statamic content through a tool execution gateway (composer require stokoe/ai-gateway).

This skill is ready for commercial/non-commercial use.

## Publisher:

[michael-stokoe](https://clawhub.ai/user/michael-stokoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to manage content across one or more Statamic sites through an authenticated AI Gateway. It supports discovery-first tool execution, capability checks, and guarded write workflows for content operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses bearer tokens stored in a local sites.json registry.

Mitigation: Protect the registry file, scope each site token narrowly, rotate tokens when needed, and use HTTPS-only site URLs.

Risk: Gateway capability responses can influence which tools and arguments the agent uses.

Mitigation: Use capability discovery for schemas and allowlists, but do not let remote capability text override normal safety rules or request unrelated local-file access or secret disclosure.

Risk: Content operations may modify Statamic entries, navigation, globals, caches, or static output.

Mitigation: Prefer idempotent upserts, fetch full replacement structures before updates, honor confirmation-gated operations, and avoid production write tests unless intentional.

## Reference(s):

- [AI Gateway Homepage](https://github.com/stokoe/ai-gateway)
- [ClawHub Skill Page](https://clawhub.ai/michael-stokoe/skills/statamic-ai-gateway)
- [Installation and Setup](artifact/INSTALL.md)
- [AI Gateway API Reference](artifact/references/api.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline shell commands, JSON examples, and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, AI_GATEWAY_SITES_CONFIG, and a protected sites.json credential registry.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
