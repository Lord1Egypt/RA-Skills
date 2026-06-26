## Description: <br>
Skill Designer guides users through requirements gathering and solution design to create a complete OpenClaw skill package without installing or modifying an agent environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shing19](https://clawhub.ai/user/shing19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to turn a proposed capability into a structured OpenClaw skill package with a SKILL.md, installation guide, and optional supporting files. It is intended for guided skill design and packaging, not automatic installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated skill files could contain incomplete, incorrect, or unsafe instructions for the target agent. <br>
Mitigation: Review the generated SKILL.md, README, and any optional scripts or references before installing or using the package. <br>
Risk: A generated output folder could overwrite or obscure earlier work if the same skill id is reused. <br>
Mitigation: Check the target output/<skill-id>/ directory before approving generation or replacement. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shing19/skill-designer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and optional supporting code or reference files in an output directory] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a bounded local skill package after user confirmation; it does not auto-install the generated skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
