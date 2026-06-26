## Description: <br>
Search the web using a self-hosted SearXNG instance with privacy-respecting metasearch across multiple engines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clockworksquirrel](https://clawhub.ai/user/clockworksquirrel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to query a self-hosted SearXNG instance, retrieve JSON search results across web categories, and format results for automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sample SearXNG configuration includes a placeholder secret key. <br>
Mitigation: Replace the placeholder secret key with a strong random value before running the service. <br>
Risk: The sample service binds to all interfaces and exposes port 8080. <br>
Mitigation: Bind to localhost or restrict network access unless remote access is intentional. <br>
Risk: The sample Docker Compose file uses an unpinned latest image tag. <br>
Mitigation: Pin the SearXNG image to a reviewed version for repeatable deployments. <br>
Risk: The sample search settings disable safe search. <br>
Mitigation: Increase safe_search when unfiltered results are not appropriate for the environment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, Docker Compose, YAML configuration, and shell function snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local service URLs, environment-variable setup, and SearXNG JSON API examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
