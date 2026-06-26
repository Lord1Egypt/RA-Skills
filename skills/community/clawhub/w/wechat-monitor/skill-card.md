## Description: <br>
微信公众号调研 + 监控 + 报告推送。每个产品独立目录，互不影响。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a1003916989-blip](https://clawhub.ai/user/a1003916989-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, operations, and content teams use this skill to research relevant WeChat public accounts for a product, monitor selected official, competitor, media, and KOL accounts, and generate recurring content-monitoring reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an mptext API key for recurring WeChat public-account monitoring. <br>
Mitigation: Configure MPTEXT_API_KEY as an environment variable, do not put the key in source files or shared workspace notes, and rotate it if the mptext login state expires. <br>
Risk: Recurring scheduled monitoring and report pushing can distribute monitored account activity to an unexpected destination. <br>
Mitigation: Confirm the selected public accounts, report delivery target, and schedule before enabling recurring pushes. <br>
Risk: Product names are used to create local product folders and report paths. <br>
Mitigation: Use simple product folder names and avoid path-like or ambiguous names. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/a1003916989-blip/wechat-monitor) <br>
- [mptext Service](https://down.mptext.top) <br>
- [mptext Public API Base](https://down.mptext.top/api/public/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with account lists, monitoring summaries, topic analysis, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MPTEXT_API_KEY for mptext API access and stores per-product account lists and Markdown reports in separate product folders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
