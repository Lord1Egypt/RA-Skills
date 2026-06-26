## Description: <br>
Financial governance for OpenClaw agents. Tracks API spend, enforces budget limits, detects runaway loops, delivers cost briefings. Reads session .jsonl logs locally. 100% private. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AnouarTrust](https://clawhub.ai/user/AnouarTrust) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and developers use this skill to review local session spending, compare model costs, enforce daily or monthly budgets, and spot runaway or unusually expensive sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw session logs, which may contain more context than cost fields. <br>
Mitigation: Use it only in environments where reading those local logs is acceptable, and avoid sharing generated reports if session names or model usage reveal sensitive work. <br>
Risk: The budget command creates or updates a local budgets.json file with spending limits. <br>
Mitigation: Review the configured daily and monthly limits after changes, and remove the local budget file if stored budget state should be reset. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration] <br>
**Output Format:** [Markdown-like cost reports with aligned summaries, warnings, progress bars, and local JSON budget configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local .jsonl session logs and may write budget settings to ~/.openclaw/workspace/trustlog-guard/budgets.json.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
