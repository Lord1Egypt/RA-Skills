## Description: <br>
Track skill versions, benchmark performance, compare improvements, and get self-improvement signals. Integrates with tasktime and ClawVault. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G9Pedro](https://clawhub.ai/user/G9Pedro) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use SkillBench to track agent skill versions, record benchmark outcomes, compare regressions or improvements, and generate signals for skill maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Benchmark records may include secrets, customer names, sensitive project names, or detailed failure messages, especially when syncing to ClawVault. <br>
Mitigation: Review benchmark content before recording or syncing; omit sensitive details and sync only data approved for ClawVault. <br>
Risk: Watch and scheduled testing can create recurring activity. <br>
Mitigation: Enable watch or schedule only when continuous monitoring is intended, and review generated cron or workflow configuration before use. <br>
Risk: The skill depends on the @versatly/skillbench npm package and the skillbench binary. <br>
Mitigation: Install only after verifying that the npm package source is trusted for your environment. <br>


## Reference(s): <br>
- [SkillBench on ClawHub](https://clawhub.ai/G9Pedro/skillbench) <br>
- [ClawVault](https://clawvault.dev) <br>
- [tasktime skill](https://clawhub.com/skills/tasktime) <br>
- [ClawHub](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, JSON, Code, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands, JSON reports, generated HTML dashboard files, badge output, and cron or workflow configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the skillbench CLI and may sync benchmark data to ClawVault when the user enables sync.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
