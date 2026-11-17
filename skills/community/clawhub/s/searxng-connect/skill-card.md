## Description:

Connect to and search the web using SearXNG, a privacy-focused meta search engine, without API keys through a self-hosted SearXNG instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rdeangel](https://clawhub.ai/user/rdeangel)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to let an agent search web, news, image, science, file, video, music, social media, and IT results through a configured SearXNG instance. It supports time filtering, language selection, safe-search control, optional full-content fetching, caching, and structured search output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches and optional full-content fetching broaden the agent's network reach beyond the configured SearXNG instance.

Mitigation: Use only a trusted SearXNG instance and avoid full-content mode in sensitive environments.

Risk: Cached search results can retain local search history.

Mitigation: Disable cache for confidential searches and treat cached results as locally retained browsing/search data.

Risk: The security review flagged the release as suspicious because network reach and caching are not fully scoped by the privacy framing.

Mitigation: Review the skill before installing and confirm the configured instance, cache settings, and search behavior match the deployment's risk tolerance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rdeangel/skills/searxng-connect)
- [uv documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON search result or error object, with optional full-content text fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and Python 3.9+; connects to the configured SearXNG instance; local cache defaults to 1 hour.]

## Skill Version(s):

1.0.0 (source: skill-config.json, README.md, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
