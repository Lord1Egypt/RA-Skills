## Description: <br>
Skill Analyst Zh helps Chinese-speaking OpenClaw users evaluate skills before installation or release by comparing similar ClawHub skills, checking overlap and security review status, and giving an installation or publication recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lixiabupt](https://clawhub.ai/user/lixiabupt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to assess whether a skill is worth installing or ready to publish. It guides comparison against installed and ClawHub skills and produces a structured recommendation report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad trigger wording around skill analysis and installation or publication advice. <br>
Mitigation: Invoke it explicitly for OpenClaw skill review tasks and review its recommendation before acting. <br>
Risk: The workflow can suggest running ClawHub CLI commands to inspect or compare skills. <br>
Mitigation: Check suggested CLI commands before execution and confirm they target the intended skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lixiabupt/skill-analyst-zh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with tables and concise recommendations; may include inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Chinese-language report templates and clear install/publish conclusions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
