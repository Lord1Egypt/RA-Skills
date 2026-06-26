## Description: <br>
Fetches public web pages through jina.ai and returns reduced markdown content to conserve context tokens for long pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qidu](https://clawhub.ai/user/qidu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need a condensed markdown version of a public page, article, README, or documentation page to reduce token use during web research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive URLs or private page contents may be exposed to jina.ai when fetched through the proxy. <br>
Mitigation: Use this skill for public pages only; avoid authenticated dashboards, intranet hosts, localhost, signed links, and URLs containing tokens unless that disclosure is intended. <br>
Risk: Reduced markdown may omit page details that matter for high-stakes decisions. <br>
Mitigation: Verify critical claims against the original source page before relying on the condensed output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qidu/web-fetch-markdown) <br>
- [jina.ai reader proxy pattern](https://r.jina.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown response from fetched public web content, with concise instructions for constructing the jina.ai proxy URL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No credentials were detected; output depends on jina.ai extraction and reduction of the source page.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
