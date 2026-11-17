## Description:

WebSearch-Openclaw helps agents search the web, fetch webpage text, and perform multi-query research through a self-hosted SearXNG instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mr-ds-ml-85](https://clawhub.ai/user/mr-ds-ml-85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve current web information, fetch readable page text, and compile lightweight research summaries using a configured SearXNG service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound web requests and fetch arbitrary URLs from the user's machine.

Mitigation: Use it only where outbound web access is acceptable, avoid private or sensitive URLs and queries, and restrict egress when handling sensitive work.

Risk: The installer creates persistent command shims and may edit shell startup files.

Mitigation: Review install.sh before running it, or use direct script execution or an isolated environment with pinned dependencies.

## Reference(s):

- [SearXNG Documentation](https://docs.searxng.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, text, JSON, and agent-oriented plain text depending on script options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include ranked search results, fetched page excerpts, source URLs, snippets, and domain frequency summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
