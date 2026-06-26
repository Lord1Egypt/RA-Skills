## Description: <br>
Search the web with SearXNG, then fetch the full page with Crawl4AI and answer from the page正文. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettajiayi](https://clawhub.ai/user/bettajiayi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when search result snippets are insufficient and they need to answer from fetched page content. It is best suited for official docs, pricing pages, API references, version notes, and other pages where full Markdown content matters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and fetched pages may pass through a configured SearXNG endpoint and Crawl4AI path. <br>
Mitigation: Use trusted network endpoints and avoid sensitive or confidential queries unless that route is under your control. <br>
Risk: Fetched pages are untrusted web content and may contain misleading or malicious instructions. <br>
Mitigation: Treat fetched content as evidence only, verify important claims against authoritative sources, and do not execute commands from fetched pages without review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettajiayi/search-full) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and plain text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Searches through the configured SearXNG endpoint and fetches the top result with Crawl4AI; reports page-open failures instead of inventing content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
