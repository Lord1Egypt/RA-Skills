## Description: <br>
Find available last-minute hotels for same-day check-in using flyai CLI results and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-support agents use this skill to search for hotels available tonight, collect destination and date filters, run flyai hotel searches, and return Markdown tables with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install the global npm package @fly-ai/flyai-cli. <br>
Mitigation: Confirm with the user before installation and prefer a pinned or manually reviewed CLI setup. <br>
Risk: Travel search details may be sent to flyai or Fliggy when live searches are executed. <br>
Mitigation: Tell users when a live search will contact an external travel service and avoid unnecessary sensitive details. <br>
Risk: The runbook can retain raw travel queries in .flyai-execution-log.json. <br>
Mitigation: Disable or delete the local execution log when local retention is not desired. <br>
Risk: Hotel answers depend on a working flyai CLI and current third-party data. <br>
Mitigation: Report CLI failures honestly and do not answer travel availability or pricing from model knowledge. <br>


## Reference(s): <br>
- [Tonight Hotel on ClawHub](https://clawhub.ai/dingtom336-gif/tonight-hotel) <br>
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Runbook](references/runbook.md) <br>
- [Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results must come from flyai CLI output, include valid booking links, and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
