## Description: <br>
Aggregates creator analytics from Toutiao, CSDN, and Zhihu dashboards and produces Markdown dashboards and reports for social media operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luduoxin](https://clawhub.ai/user/luduoxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and social media operators use this skill to collect follower, readership, content, and earnings metrics from their own logged-in creator dashboards and turn them into concise Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a logged-in browser and read private creator dashboard data, including earnings and browser profile data. <br>
Mitigation: Use a separate browser profile when possible, review each browser automation step before running it, and close Chrome debugging mode after use. <br>
Risk: Copied dashboard data may contain private or sensitive account information. <br>
Mitigation: Review and redact collected dashboard data before sending it to an AI or sharing generated reports. <br>
Risk: Raw cookies or login credentials could expose creator accounts if shared. <br>
Mitigation: Avoid sharing raw cookies, login credentials, or exported browser profile data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luduoxin/social-media-dashboard) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Toutiao collection notes](artifact/platforms/toutiao.md) <br>
- [CSDN collection notes](artifact/platforms/csdn.md) <br>
- [Zhihu collection notes](artifact/platforms/zhihu.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser automation steps, extracted dashboard metrics, JSON snippets, and report templates.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
