## Description: <br>
Analyze and evaluate OpenClaw skills before installing or publishing, compare against existing or ClawHub skills, check feature overlap, perform security review, and provide clear install/publish recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lixiabupt](https://clawhub.ai/user/lixiabupt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to evaluate whether an OpenClaw skill is worth installing or ready to publish by comparing alternatives, checking overlap, reviewing risk, and producing a concise recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Overlap analysis may expose names and descriptions of locally installed skills to the active agent context. <br>
Mitigation: Use `clawhub list` or a narrow SKILL.md read when possible, and run the analysis only in workspaces where sharing installed skill metadata is acceptable. <br>
Risk: The workflow relies on local `clawhub` and optional `skill-vetter` tools. <br>
Mitigation: Use trusted installations of those tools and review proposed shell commands before running them. <br>


## Reference(s): <br>
- [Skill Analyst on ClawHub](https://clawhub.ai/lixiabupt/skill-analyst) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ends with a clear install or publish verdict.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
