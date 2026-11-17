## Description:

Install an OpenClaw plugin that adds SearXNG-powered web search without paid search APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barrontang](https://clawhub.ai/user/barrontang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install and configure a SearXNG-backed search tool so agents can retrieve web search results from a trusted local or remote SearXNG instance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the plugin depends on npm package trust and package provenance.

Mitigation: Install only from a trusted publisher, prefer pinning an exact version, and verify package provenance before deployment.

Risk: Search queries are sent to the configured SearXNG instance and may contain sensitive information.

Mitigation: Use a SearXNG instance you control or trust, and avoid sending sensitive or regulated queries to untrusted servers.

Risk: Returned web results may be incomplete, stale, or misleading.

Mitigation: Have agents cite and cross-check important results before using them for consequential decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/barrontang/skills/searxng-tool-for-openclaw)
- [Homepage](https://github.com/barrontang/searxng-tool-for-openclaw)
- [Repository](https://github.com/barrontang/searxng-tool-for-openclaw)
- [Documentation](https://github.com/barrontang/searxng-tool-for-openclaw#readme)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration; tool responses are structured JSON search results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw and a reachable SearXNG instance with JSON output enabled; result limits and timeout are configurable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
