## Description: <br>
Fetches a specific web page URL through a configured OpenClaw Manager Web Fetch Proxy and returns parsed page content as Markdown or plain text with metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whyhit2005](https://clawhub.ai/user/whyhit2005) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to read a known web page URL, convert the page to Markdown or text, and optionally include page metadata, images, link summaries, or image summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-selected URLs are sent through the configured OpenClaw Manager Web Fetch Proxy. <br>
Mitigation: Use only a trusted proxy and avoid private documents, secret-bearing links, tokenized URLs, localhost or private-network addresses, and regulated content unless appropriate logging, retention, and network controls are in place. <br>
Risk: The skill depends on WEB_FETCH_PROXY_URL and curl being available. <br>
Mitigation: Configure WEB_FETCH_PROXY_URL and verify curl is installed before enabling the skill for agent workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/whyhit2005/proxy-web-fetch) <br>
- [Publisher profile](https://clawhub.ai/user/whyhit2005) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration] <br>
**Output Format:** [JSON response containing parsed page content, metadata, and Markdown or plain-text body content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and WEB_FETCH_PROXY_URL; supports timeout, cache, image retention, GFM, image summary, and link summary options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
