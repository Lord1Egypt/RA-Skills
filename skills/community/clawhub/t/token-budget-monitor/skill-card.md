## Description: <br>
Track and control token consumption across OpenClaw cron jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aviclaw](https://clawhub.ai/user/aviclaw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to monitor token usage across OpenClaw cron jobs, sessions, and fallback chains, with daily and per-job budget checks, alerts, and model recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool stores local records of job names, model names, run counts, and token totals. <br>
Mitigation: Review where the local OpenClaw workspace output file is stored and avoid recording sensitive job or model identifiers. <br>
Risk: The documented exec integration pattern can be risky if untrusted values are interpolated into shell commands. <br>
Mitigation: Use an argument-array API such as spawn or execFile, or strictly validate job and model names before passing them to the tracker. <br>
Risk: Budget checks and model recommendations are monitoring support, not automatic enforcement. <br>
Mitigation: Keep separate enforcement controls for jobs that must stop or change models when budgets are exceeded. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aviclaw/token-budget-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output and local JSON usage log] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes token usage records to a local token-usage.json file under the user's OpenClaw workspace outputs directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
