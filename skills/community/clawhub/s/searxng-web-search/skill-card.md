## Description: <br>
Search the web using a self-hosted SearXNG metasearch engine for online information, recent news, topic research, and current internet context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gangtao](https://clawhub.ai/user/gangtao) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and agent users use this skill to route web search requests through a configured SearXNG instance and receive structured search results for downstream reasoning or reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to the configured SearXNG service. <br>
Mitigation: Use a trusted or self-hosted SearXNG endpoint, prefer HTTPS for non-local servers, and avoid sending secrets or sensitive private terms in queries. <br>
Risk: Deployment examples can expose a local SearXNG service if network binding is not hardened. <br>
Mitigation: Bind local SearXNG services to localhost unless intentionally securing them for network access. <br>


## Reference(s): <br>
- [SearXNG Reference Guide](references/REFERENCE.md) <br>
- [SearXNG Documentation](https://docs.searxng.org/) <br>
- [ClawHub skill page](https://clawhub.ai/gangtao/searxng-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results, markdown guidance, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search result JSON includes query, results, suggestions, answers, total_results, and error fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
