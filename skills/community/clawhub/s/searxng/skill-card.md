## Description: <br>
Privacy-respecting metasearch using your local SearXNG instance. Search the web, images, news, and more without external API dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abk234](https://clawhub.ai/user/abk234) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to search the web, images, videos, news, and other SearXNG categories through a configured local, private, or public SearXNG instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to the configured SearXNG instance, which may be public or operated by another party. <br>
Mitigation: Use localhost or a trusted private SearXNG instance and avoid searching secrets or sensitive internal data. <br>
Risk: The artifact disables TLS certificate verification to support local self-signed deployments. <br>
Mitigation: Enable strict TLS verification before using a remote HTTPS SearXNG instance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abk234/searxng) <br>
- [SearXNG homepage](https://searxng.org) <br>
- [SearXNG documentation](https://docs.searxng.org/) <br>
- [SearXNG installation guide](https://docs.searxng.org/admin/installation.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime search results as terminal tables or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a configured SEARXNG_URL; default target is http://localhost:8080.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter and changelog show 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
