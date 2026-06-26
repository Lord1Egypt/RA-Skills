## Description: <br>
Create new skills, modify and improve existing skills, and measure skill performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tlreal](https://clawhub.ai/user/tlreal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to create, edit, test, evaluate, and optimize agent skills through an iterative workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create or modify other skills, which may introduce incorrect instructions or unintended behavior if accepted without review. <br>
Mitigation: Review generated or modified skills before making them active, and keep trigger descriptions specific. <br>
Risk: Evaluation workflows may involve helper scripts, subagents, browser viewers, or MCPs that process project data. <br>
Mitigation: Only run helper scripts from a trusted skill-creator directory and avoid using sensitive project data with untrusted MCPs, subagents, or browser viewers. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON, code, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify skill files and evaluation artifacts when used by an agent with filesystem access.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
