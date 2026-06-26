## Description: <br>
Privacy-respecting metasearch using your local SearXNG instance for web, image, news, video, and other searches without external API dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phucanh08](https://clawhub.ai/user/phucanh08) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to query a configured SearXNG instance for web, image, video, news, map, music, file, IT, and science search results without relying on a commercial search API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to the configured SearXNG instance, which may expose sensitive query text if the instance is not trusted. <br>
Mitigation: Use a local or otherwise trusted SearXNG instance and avoid sending secrets or sensitive internal text as search queries. <br>
Risk: Remote HTTPS instances may involve TLS trust caveats, especially when using self-signed certificates. <br>
Mitigation: Prefer trusted certificate setups or enable strict TLS verification when connecting to remote HTTPS instances. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phucanh08/searxng-1) <br>
- [SearXNG project](https://searxng.org) <br>
- [SearXNG installation documentation](https://docs.searxng.org/admin/installation.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown/text guidance, terminal tables, and JSON search result payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a configured SEARXNG_URL; defaults to http://localhost:8080.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
