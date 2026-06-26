## Description: <br>
Audits installed skills for quality, duplicates, structural issues, and best-practice compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bill492](https://clawhub.ai/user/bill492) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to audit installed OpenClaw skills for structural quality, duplicates, stale files, and category coverage before publishing or maintaining a skill set. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated audit report may include local skill names and filesystem paths. <br>
Mitigation: Review the report before sharing, publishing, or committing it. <br>
Risk: The skill runs a local shell script to inspect configured skill directories. <br>
Mitigation: Run it only in environments where installed skill metadata may be inspected. <br>


## Reference(s): <br>
- [Skill Audit on ClawHub](https://clawhub.ai/bill492/unblocklabs-skill-audit) <br>
- [Anthropic: Lessons from Building Claude Code Skills](https://x.com/trq212/status/2033949937936085378) <br>
- [Ole Lehmann: Auto-improve Skills](https://x.com/itsolelehmann/status/2033919415771713715) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report and chat summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes .sub-agent-results/skill-audit-report.md; the report may include local skill names and filesystem paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
