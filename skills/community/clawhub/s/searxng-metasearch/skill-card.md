## Description:

Search the web using a self-hosted SearXNG instance. Privacy-respecting metasearch that aggregates results from multiple engines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clockworksquirrel](https://clawhub.ai/user/clockworksquirrel)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to configure and query a self-hosted SearXNG service for privacy-respecting web search results in JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides users to run a local Docker service that could be exposed beyond the local machine if configured broadly.

Mitigation: Bind the service to 127.0.0.1 unless LAN or internet access is intentional, and restrict access with firewall rules before starting it.

Risk: The example configuration contains a placeholder server secret.

Mitigation: Replace the placeholder secret with a random value before use.

Risk: Using a floating container image tag can pull changed software over time.

Mitigation: Pin the SearXNG image to a trusted version or digest.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Docker setup guidance, SearXNG query examples, JSON response field descriptions, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
