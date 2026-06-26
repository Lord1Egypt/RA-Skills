## Description: <br>
Search the web using a self-hosted SearXNG instance. Privacy-respecting metasearch that aggregates results from multiple engines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grakeshk-max](https://clawhub.ai/user/grakeshk-max) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to send search queries through a configured self-hosted SearXNG instance and receive JSON search results from aggregated engines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to the configured SearXNG endpoint and may be forwarded to upstream engines selected by that instance. <br>
Mitigation: Use only trusted SearXNG instances and review the configured engines, retention, and logging policies before use. <br>
Risk: A publicly exposed SearXNG instance can leak queries or invite unwanted access if deployed without protection. <br>
Mitigation: Keep the service local where possible, or protect it with HTTPS, authentication, and a strong non-default secret key. <br>
Risk: Using an unpinned Docker image can change runtime behavior when the image is updated. <br>
Mitigation: Pin the SearXNG image version for controlled deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/grakeshk-max/searxng-local-search-v1) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance, Configuration] <br>
**Output Format:** [JSON search results from a SearXNG HTTP endpoint, with Markdown setup guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include title, URL, content snippet, engines, score, and category when returned by SearXNG.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
