## Description: <br>
Understand what your AI agent's skills are actually being used for, with usage reports, success/failure tracking, and unused-skill recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yingy4](https://clawhub.ai/user/yingy4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Skill Insight to analyze local skill usage records, report usage and outcomes, and identify skills that may be unused or unreliable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session scanning and recurring tracking can inspect local OpenClaw session content and summarize usage into local logs. <br>
Mitigation: Enable scanning, cron, or HEARTBEAT-style recording only when local usage analytics are intended; avoid recording secrets in scenes or notes and remove scheduled tracking when it is no longer needed. <br>
Risk: The skill cannot automatically detect route-type skill calls and can produce empty or incomplete reports when usage data is not collected. <br>
Mitigation: Configure manual or agent-assisted recording for route-type skills and treat reports as coverage-limited analytics rather than complete telemetry. <br>


## Reference(s): <br>
- [Skill Insight ClawHub release page](https://clawhub.ai/yingy4/skill-insight) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or terminal text reports, with optional JSON report output and shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports English and Chinese report output; reads and writes local usage and registry JSON files.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
