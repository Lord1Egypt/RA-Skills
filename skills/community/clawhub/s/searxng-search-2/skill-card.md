## Description: <br>
Web search using SearXNG instance via MCP. Provides web search capability for agents with configurable SearXNG endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zfanmy](https://clawhub.ai/user/zfanmy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agent users use this skill to add SearXNG-backed web search to agents through an MCP server or shell script with configurable result limits and text, JSON, or Markdown output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and result handling depend on the configured SearXNG endpoint, which may receive private or sensitive query text. <br>
Mitigation: Use only trusted SearXNG endpoints, prefer HTTPS for remote servers, and avoid searching secrets or private project data. <br>
Risk: Copying the included MCP configuration can overwrite or disturb an existing mcporter setup. <br>
Mitigation: Merge or back up existing mcporter configuration before copying this package's config.json. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zfanmy/searxng-search-2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Search results returned as plain text, Markdown, or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured SEARXNG_URL endpoint and supports a result limit.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
