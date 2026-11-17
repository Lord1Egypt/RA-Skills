## Description:

Self-hosted web search aggregator for OpenClaw agents that can install a local SearXNG service or run searches against an existing local instance without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saikatkumardey](https://clawhub.ai/user/saikatkumardey)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add web search capability to OpenClaw agents by installing and managing a local SearXNG service, or by using the included CLI to query an existing local SearXNG instance. It is also useful for diagnosing search failures and understanding fallback behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer uses root privileges to fetch mutable third-party code and enable a persistent local search service.

Mitigation: Run it only on hosts where root-level setup and a persistent local service are acceptable, and review or modify the installer to pin and verify SearXNG, uv, and dependencies before production use.

Risk: Fallback mode sends search queries to Wikipedia and GitHub, which can expose sensitive prompts or internal identifiers.

Mitigation: Avoid sensitive query content, or disable or modify fallback behavior for confidential workloads.

## Reference(s):

- [SearXNG Search Usage Reference](references/usage.md)
- [SearXNG source repository](https://github.com/searxng/searxng)
- [ClawHub skill page](https://clawhub.ai/saikatkumardey/skills/searxng-selfhost)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python CLI output, and optional JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include title, URL, snippet, and engine fields when emitted as JSON.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
