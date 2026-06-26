## Description: <br>
Monitor multiple WeChat public-account RSS feeds for AI and technology articles, filter recent items by keyword, and generate local Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pyh-pan](https://clawhub.ai/user/pyh-pan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and analysts use this skill to monitor configured WeChat-related RSS sources for AI and technology coverage from the past 24 hours and collect matching articles into daily Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured RSS feeds can return untrusted or misleading article text that is copied into reports. <br>
Mitigation: Review configured RSS URLs before use and treat generated report content as untrusted external feed text. <br>
Risk: The skill depends on the Python requests package for network fetching. <br>
Mitigation: Pin or update the requests dependency in the execution environment according to local dependency-management policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pyh-pan/wechat-ai-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown report written to a local file, with console status output and JSON configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are generated from enabled RSS accounts configured in ~/.config/wechat-monitor/accounts.json and saved under ~/.config/wechat-monitor/reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
