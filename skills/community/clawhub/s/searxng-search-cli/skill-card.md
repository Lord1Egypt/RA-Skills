## Description:

Uses a self-hosted SearXNG search engine to provide agents with free, multi-engine web search through a CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeshunee](https://clawhub.ai/user/leeshunee)

### License/Terms of Use:

GNU General Public License v3.0

## Use Case:

Developers and agents use this skill to deploy or connect to a SearXNG instance and run aggregated web searches without a paid search API. It is suited for information retrieval, project research, and self-hosted search workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute remote installation code, install mutable upstream software, and run a local SearXNG service.

Mitigation: Review installer commands before execution, pin or verify uv, SearXNG, and dependencies where possible, and approve any sudo use explicitly.

Risk: Search queries can be sent to the local SearXNG instance and upstream search engines.

Mitigation: Avoid searching for secrets, private data, or sensitive internal information.

Risk: The setup path can create persistence for the local SearXNG service.

Mitigation: Use the status, enable, disable, start, and stop commands deliberately and document whether auto-start is appropriate for the host.

## Reference(s):

- [SearXNG Search CLI Onboarding](references/ONBOARDING.md)
- [SearXNG Official Docs](https://docs.searxng.org)
- [SearXNG GitHub Repository](https://github.com/searxng/searx)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI search result text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results depend on the configured SearXNG instance and upstream search engines.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
