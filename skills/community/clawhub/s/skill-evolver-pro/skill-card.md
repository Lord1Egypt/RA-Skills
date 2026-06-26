## Description: <br>
Analyzes skill usage, errors, feedback, and performance signals to produce optimization plans, Markdown reports, evolution state tracking, and resumable multi-stage improvement workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pagoda111king](https://clawhub.ai/user/pagoda111king) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to evaluate agent-skill performance, identify shortcomings, generate prioritized improvement plans, and resume long-running evolution workflows from persisted state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists telemetry, evolution history, and state data on disk. <br>
Mitigation: Use a dedicated data directory with restricted permissions and review stored logs before sharing or publishing them. <br>
Risk: Raw logs, feedback, prompts, customer content, or stack traces may contain sensitive data. <br>
Mitigation: Redact secrets, personal data, customer content, prompts, and detailed stack traces before passing inputs into the evolution pipeline. <br>
Risk: Generated optimization plans may be incomplete or unsuitable for a specific skill. <br>
Mitigation: Review proposed changes, run tests, and scan updated skill files before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pagoda111king/skill-evolver-pro) <br>
- [Publisher profile](https://clawhub.ai/user/pagoda111king) <br>
- [Usage examples](artifact/examples/usage-examples.md) <br>
- [Version history](artifact/VERSION_HISTORY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON state/log data, JavaScript modules, and structured plan objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes evolution logs, version history, and resumable state data to local storage.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and artifact version history, released 2026-04-13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
