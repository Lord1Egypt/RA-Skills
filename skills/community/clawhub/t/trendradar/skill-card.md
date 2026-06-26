## Description: <br>
TrendRadar scans social media and community sources to identify rising product trends and timing signals before they peak. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and consumers use this skill to scan public trend sources for products that are surging, rising, stable, or cooling, then decide whether to analyze, buy, wait, or skip. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may activate the skill when the user did not intend to run product trend scanning. <br>
Mitigation: Review or narrow the trigger phrases before installation if accidental activation would be disruptive. <br>
Risk: The daily briefing command can create recurring notifications if scheduled through cron. <br>
Mitigation: Add the cron job only when recurring daily trend briefings are desired, and choose the intended channel and region options. <br>
Risk: The skill depends on live public web and community sources, so trend signals can be incomplete, stale, or platform-dependent. <br>
Mitigation: Treat outputs as decision support and verify important purchases or business decisions against current source pages before acting. <br>


## Reference(s): <br>
- [TrendRadar on ClawHub](https://clawhub.ai/jiajiaoy/trendradar) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Artifact README](README.md) <br>
- [Artifact Skill Definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown trend briefings with source links, trend direction labels, commercial signals, and suggested OpenClaw commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports keyword or all-category scans, region selection for cn/us/global/all, and zh/en output language.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
