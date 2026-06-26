## Description: <br>
Helps an agent turn successful complex tasks into reusable skills for ongoing procedural memory and knowledge accumulation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tunsuy](https://clawhub.ai/user/tunsuy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to decide when a completed complex workflow should be captured as a reusable skill, then scaffold, maintain, and validate the skill files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to create or overwrite reusable skill files. <br>
Mitigation: Use a dedicated skills directory and require review before creating or overwriting files. <br>
Risk: Generated scripts or commands may be unsafe or unsuitable for the user's environment. <br>
Mitigation: Inspect generated scripts and commands before running them. <br>
Risk: Incorrect guidance could be preserved as reusable procedural memory. <br>
Mitigation: Review and validate new or updated skills before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tunsuy/self-evolving-skills) <br>
- [Publisher profile](https://clawhub.ai/user/tunsuy) <br>
- [Decision Flow](artifact/references/decision-flow.md) <br>
- [Skill Format](artifact/references/skill-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional code blocks, file templates, and validation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed file paths and generated skill content for review before writing or execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
