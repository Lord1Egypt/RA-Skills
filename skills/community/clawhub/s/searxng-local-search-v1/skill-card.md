## Description:

Search the web using a self-hosted SearXNG instance. Privacy-respecting metasearch that aggregates results from multiple engines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grakeshk-max](https://clawhub.ai/user/grakeshk-max)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to let an agent query a self-hosted SearXNG instance and return metasearch results while keeping search infrastructure under their control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to the configured SearXNG endpoint.

Mitigation: Run SearXNG locally or use a trusted HTTPS endpoint, and treat queries as data visible to that server.

Risk: The example SearXNG configuration includes a placeholder secret key.

Mitigation: Replace the sample secret key with a strong random value before use.

Risk: The example Docker setup uses a mutable latest image tag.

Mitigation: Pin or verify the SearXNG Docker image before deployment.

Risk: A remote or publicly exposed SearXNG service can create transport and access-control risk.

Mitigation: Prefer loopback binding for local use, or require HTTPS and authentication for remote access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/grakeshk-max/skills/searxng-local-search-v1)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [SearXNG JSON search response, typically summarized by the agent in text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search is configured with an optional SEARXNG_URL endpoint and supports category selection for general, images, news, videos, it, and science searches.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
