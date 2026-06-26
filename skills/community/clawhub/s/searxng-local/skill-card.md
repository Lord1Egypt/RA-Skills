## Description: <br>
Search the web using a self-hosted SearXNG instance. Privacy-respecting metasearch that aggregates results from multiple engines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clockworksquirrel](https://clawhub.ai/user/clockworksquirrel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure and query a local or self-hosted SearXNG service for privacy-respecting web search results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Docker setup can expose a persistent SearXNG service on port 8080. <br>
Mitigation: Restrict access to port 8080 when the host is reachable by others and review the service before deployment. <br>
Risk: The sample SearXNG configuration uses a placeholder secret key and safe_search set to 0. <br>
Mitigation: Change the example secret key before use and raise safe_search if unfiltered results are not appropriate. <br>
Risk: The Docker image tag is not pinned in the example compose file. <br>
Mitigation: Pin the Docker image version when reproducibility or change control is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/clockworksquirrel/searxng-local) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the optional SEARXNG_URL environment variable and SearXNG JSON responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
