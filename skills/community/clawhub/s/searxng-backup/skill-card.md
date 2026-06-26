## Description: <br>
Privacy-respecting metasearch using a configured SearXNG instance for web, image, news, video, and other search categories without external API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[macdesire](https://clawhub.ai/user/macdesire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route agent search requests through a SearXNG instance they control or trust, with options for category, language, recency, result count, and JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to the configured SearXNG server, which may expose sensitive queries if the server is public or untrusted. <br>
Mitigation: Use a local or trusted self-hosted SearXNG instance, and avoid sensitive searches on public instances. <br>
Risk: The artifact disables TLS certificate verification in the HTTP request path. <br>
Mitigation: Enable certificate verification before relying on a remote HTTPS endpoint, or keep the endpoint local and trusted. <br>


## Reference(s): <br>
- [SearXNG Project](https://searxng.org) <br>
- [SearXNG Installation Guide](https://docs.searxng.org/admin/installation.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/macdesire/searxng-backup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON] <br>
**Output Format:** [Rich terminal table output or JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a configured SEARXNG_URL; supports result limit, category, language, and time-range options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
