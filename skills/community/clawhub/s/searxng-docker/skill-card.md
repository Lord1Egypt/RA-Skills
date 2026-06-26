## Description: <br>
Search the web through a local self-hosted SearXNG instance, with support for categories, language, time filters, selected engines, and JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[triwinds](https://clawhub.ai/user/triwinds) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run web searches through a local SearXNG Docker service when they need metasearch results, news, images, videos, IT, science, language filters, or structured JSON results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires running a persistent local Docker search service. <br>
Mitigation: Install only when that local service posture is acceptable and review the Docker Compose configuration before deployment. <br>
Risk: Exposing the SearXNG service beyond localhost can broaden network access to the search endpoint. <br>
Mitigation: Keep the default localhost binding unless deliberate exposure is required and protected. <br>
Risk: The Docker Compose file uses the latest SearXNG image tag. <br>
Mitigation: Pin the container image version for repeatable production deployments. <br>
Risk: Search terms and results can be sent to configured search engines or a remote SearXNG instance. <br>
Mitigation: Avoid sensitive search terms and use --base-url only with SearXNG instances you trust. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/triwinds/searxng-docker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output may include result titles, URLs, snippets, source engines, scores, and published dates when returned by SearXNG.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
