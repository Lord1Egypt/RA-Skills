## Description:

Agent-first web search and retrieval for live web search, news search, docs lookup, code lookup, company research, site crawl, site map, and structured evidence packs, with a no-key baseline and optional provider integrations for wider coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjianru](https://clawhub.ai/user/zjianru)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run live search, news search, documentation lookup, code lookup, extraction, crawl, site map, and research-pack workflows from a local Node runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network retrieval could expose private network targets or provider API credentials in some configurations.

Mitigation: Review before installing in environments with internal HTTP services, cloud metadata, or valuable provider keys, and run with network restrictions where possible.

Risk: Search text, target URLs, and retrieval requests may be sent to configured external providers or custom gateways.

Mitigation: Use only trusted provider credentials and gateway endpoints, and avoid sensitive search text unless provider transmission is acceptable.

Risk: Custom gateway overrides can change where retrieval traffic and credentials are sent.

Mitigation: Disable custom gateway overrides unless the endpoint is trusted and intentionally configured.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zjianru/skills/web-search-pro)
- [Publisher profile](https://clawhub.ai/user/zjianru)
- [Artifact-declared project homepage](https://github.com/Zjianru/web-search-pro)
- [ClawHub compliance notes](docs/clawhub-compliance.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and retrieval outputs may include provider routing summaries, cache telemetry, extracted page text, crawl maps, and structured research packs.]

## Skill Version(s):

2.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
