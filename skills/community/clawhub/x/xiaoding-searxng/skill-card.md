## Description: <br>
Privacy-respecting metasearch using your local SearXNG instance. Search the web, images, news, and more without external API dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asterisk622](https://clawhub.ai/user/asterisk622) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to search web, image, news, and other SearXNG categories through a configured local or trusted SearXNG instance without relying on a commercial search API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may be sent to an untrusted or public SearXNG instance. <br>
Mitigation: Configure SEARXNG_URL to a trusted local or remote instance and avoid sensitive queries on public instances. <br>
Risk: The Docker helper can remove an existing container named searxng and start a persistent host-networked service. <br>
Mitigation: Review run-searxng.sh before use and run it only when replacing that container and exposing the service on the host network is intended. <br>
Risk: Remote HTTPS requests are made with certificate verification disabled in the artifact script. <br>
Mitigation: For remote HTTPS instances, enable certificate verification or restrict use to trusted local/self-signed deployments where this behavior is understood. <br>


## Reference(s): <br>
- [SearXNG homepage](https://searxng.org) <br>
- [SearXNG installation guide](https://docs.searxng.org/admin/installation.html) <br>
- [SearXNG settings documentation](https://docs.searxng.org/admin/settings/settings.html) <br>
- [ClawHub skill page](https://clawhub.ai/asterisk622/xiaoding-searxng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Formatted search-result tables, JSON search-result objects, and concise setup or troubleshooting guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a configured SEARXNG_URL; direct CLI use can select category, result limit, language, time range, and table or JSON output.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
