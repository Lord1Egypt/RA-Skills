## Description: <br>
Query, analyze, and track skill usage information across Claude Code and OpenClaw environments, including call counts, success rates, last-used times, redundant installations, duplicates, and available skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leo-306](https://clawhub.ai/user/leo-306) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect local Claude Code and OpenClaw skill usage, find unused or duplicate skills, and prioritize cleanup or troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans local Claude Code and OpenClaw session history and can retain aggregate usage records that include project paths. <br>
Mitigation: Install and run it only where local session-history scanning is acceptable, and review or delete the generated stats files when that retained history is not wanted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leo-306/skill-stats) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Console text with Markdown table guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill writes local aggregate statistics files for Claude Code and OpenClaw environments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
