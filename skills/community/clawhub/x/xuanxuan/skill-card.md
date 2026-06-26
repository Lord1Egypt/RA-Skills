## Description: <br>
Skill Tracker helps agents track skill usage, calculate health scores, generate optimization suggestions, and produce Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alsoforever](https://clawhub.ai/user/alsoforever) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to collect local OpenClaw skill usage records, calculate health scores, generate improvement proposals, and produce Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Usage metadata could include sensitive prompts, credentials, customer data, tokens, or file contents if callers pass that information into the logging metadata. <br>
Mitigation: Keep logged metadata minimal and exclude secrets, prompts, customer data, tokens, and sensitive file contents. <br>
Risk: Optional cron jobs can create ongoing local telemetry and scheduled analysis artifacts. <br>
Mitigation: Enable scheduled jobs only when continuous local tracking is desired, and review generated logs and reports regularly. <br>
Risk: Generated optimization proposals may be incorrect or misleading if based on sparse or noisy usage records. <br>
Mitigation: Review proposals before changing, removing, or rewriting skills. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/alsoforever/xuanxuan) <br>
- [Skill definition](SKILL.md) <br>
- [Open-source README](README-opensource.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, Markdown reports, JSON health snapshots, and JSONL usage logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local usage records, health snapshots, proposals, and scheduled analysis logs when the included scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
