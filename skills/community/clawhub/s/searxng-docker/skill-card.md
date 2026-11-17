## Description:

SearXNG Docker helps agents search the web through a local, self-hosted SearXNG instance with category, language, time-range, engine, and JSON-output options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[triwinds](https://clawhub.ai/user/triwinds)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run a local SearXNG service and query it for general web, news, image, video, IT, science, file, or social media search results without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts a persistent local Dockerized SearXNG service and uses an unpinned container image.

Mitigation: Pin the SearXNG container image to a reviewed version or digest before production use, and stop the Docker service when it is no longer needed.

Risk: Search requests may still reach configured upstream search engines.

Mitigation: Review the enabled engines and privacy expectations before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/triwinds/skills/searxng-docker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands, configuration files, and optional JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output can be human-readable text or compact JSON containing result title, URL, content, engines, score, and published date.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
