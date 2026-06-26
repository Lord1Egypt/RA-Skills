## Description: <br>
Search the web using a self-hosted SearXNG instance. Privacy-respecting metasearch that aggregates results from multiple engines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clockworksquirrel](https://clawhub.ai/user/clockworksquirrel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to configure and query a self-hosted SearXNG instance for privacy-respecting metasearch with JSON output for automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A SearXNG service exposed beyond the local computer can make search access available to other network users. <br>
Mitigation: For local-only use, bind Docker to 127.0.0.1 and review network exposure before installation. <br>
Risk: The sample configuration uses a placeholder secret key and an unpinned Docker image tag. <br>
Mitigation: Replace the placeholder secret key with a random value and consider pinning the Docker image version. <br>
Risk: Search terms pass through the configured SearXNG instance and the upstream search engines it queries. <br>
Mitigation: Review the privacy posture of the configured instance and avoid sending sensitive queries unless that routing is acceptable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, Docker Compose, YAML, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance depends on a reachable SearXNG service and optional SEARXNG_URL environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
