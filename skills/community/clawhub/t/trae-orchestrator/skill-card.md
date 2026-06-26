## Description: <br>
Orchestrates TRAE IDE for automated software development with multi-agent collaboration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Vichard998](https://clawhub.ai/user/Vichard998) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project leads use this skill to create project scaffolding, generate TRAE prompts, launch TRAE, monitor progress signals, and coordinate automated software development workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create local files, launch TRAE, and submit prompts through desktop automation. <br>
Mitigation: Use it only in a fresh or version-controlled project directory and review generated changes before running them. <br>
Risk: Desktop automation has weak targeting and may send prompts to the wrong focused window. <br>
Mitigation: Confirm the TRAE executable path and focused window before enabling auto-send. <br>
Risk: Prompts sent into TRAE may expose sensitive information. <br>
Mitigation: Avoid placing secrets or confidential data in prompts or generated project documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Vichard998/trae-orchestrator) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Implementation notes](artifact/INNOVATIONS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, file-based control signals, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local project files, TRAE prompts, control signals, and status summaries for agent-assisted development.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
