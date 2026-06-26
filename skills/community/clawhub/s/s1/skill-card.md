## Description: <br>
Provides web search, URL crawling, news, sitemap discovery, trending topics, and reasoning workflows through the Search1API s1 CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fatwang2](https://clawhub.ai/user/fatwang2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve current web information, summarize URLs, inspect site links, gather news, explore trending topics, and synthesize research from Search1API CLI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, URLs, crawled pages, or reasoning prompts may be sent to Search1API as a third-party web access provider. <br>
Mitigation: Use a dedicated API key where possible and avoid sending credentials, confidential documents, regulated data, private URLs, or sensitive personal information unless that transfer is intentional. <br>
Risk: The skill depends on a third-party npm CLI and paid API credits. <br>
Mitigation: Verify the search1api-cli package before global installation and monitor API usage or credit costs. <br>


## Reference(s): <br>
- [Usage examples](reference/examples.md) <br>
- [Search1API](https://search1api.com) <br>
- [ClawHub skill page](https://clawhub.ai/fatwang2/s1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the s1 CLI and SEARCH1API_KEY; Search1API commands may return human-readable output or raw JSON with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
