## Description: <br>
Web extraction for LLMs and agents that scrapes, crawls, maps, searches, extracts, summarizes, diffs, monitors, and researches URLs into clean Markdown, text, or JSON, including pages that block bots or render with JavaScript. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xmassi](https://clawhub.ai/user/0xmassi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use webclaw to retrieve, crawl, search, extract, summarize, diff, monitor, and structure web content for downstream LLM workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Target URLs, search queries, extraction prompts, page content, and monitor results may be sent to Webclaw's cloud service. <br>
Mitigation: Use only data approved for third-party processing; avoid secrets, internal or private URLs, customer data, and other sensitive content. <br>
Risk: Persistent watch and webhook features can create ongoing external data flows. <br>
Mitigation: Review webhook destinations and delete monitors when they are no longer needed. <br>
Risk: Endpoint discovery can enumerate API surfaces on sites where the user may not have authorization. <br>
Mitigation: Run endpoint discovery only on sites and scopes where enumeration is authorized. <br>
Risk: The skill relies on a Webclaw API key for cloud calls. <br>
Mitigation: Store WEBCLAW_API_KEY in an approved secret mechanism, avoid committing it, and rotate it if exposed. <br>


## Reference(s): <br>
- [Webclaw homepage](https://webclaw.io) <br>
- [ClawHub skill page](https://clawhub.ai/0xmassi/webclaw-extraction) <br>
- [Webclaw API base](https://api.webclaw.io/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown, plain text, JSON API responses, and CLI command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WEBCLAW_API_KEY for cloud API calls; the bundled wrapper can perform local extraction for simple public pages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
