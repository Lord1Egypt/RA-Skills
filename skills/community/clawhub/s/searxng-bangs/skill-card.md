## Description: <br>
Privacy-respecting web search via SearXNG with DuckDuckGo-style bangs, multi-category search, and JSON search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rpeters511](https://clawhub.ai/user/rpeters511) <br>

### License/Terms of Use: <br>
CC0 <br>


## Use Case: <br>
Developers and agents use this skill to run privacy-focused web, news, image, video, and science searches through a configured SearXNG instance. It is useful when search queries should avoid direct tracking by commercial search engines or when DuckDuckGo-style bangs are needed for engine-specific searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to the configured SearXNG endpoint, so unknown public instances can observe queries. <br>
Mitigation: Use a self-hosted or reputable HTTPS SearXNG instance for privacy-sensitive searches, and avoid sensitive queries through untrusted public instances. <br>
Risk: Container installs that use a floating Docker tag may change over time. <br>
Mitigation: Pin the SearXNG Docker image version or digest when reproducible deployments are required. <br>


## Reference(s): <br>
- [SearXNG API Reference](references/api.md) <br>
- [SearXNG public instances](https://searx.space) <br>
- [SearXNG installation documentation](https://docs.searxng.org/admin/installation.html) <br>
- [ClawHub package page](https://clawhub.ai/rpeters511/searxng-bangs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results with titles, URLs, and snippets; Markdown guidance and shell commands for setup and usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the SEARXNG_URL environment variable to select a self-hosted or public SearXNG instance; default timeout is 15 seconds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
