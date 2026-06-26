## Description: <br>
Distill chat history and social material into a local Simp Dog agent skill with generated memory and persona files that can be updated over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brother-yang](https://clawhub.ai/user/brother-yang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to create entertainment-oriented character skills from user-supplied relationship memories, chat exports, social posts, screenshots, and corrections. The skill guides intake, analyzes source material, and writes local memory, persona, metadata, and SKILL.md files for each generated character. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive relationship-derived data can be stored persistently in generated memory, persona, metadata, and skill files. <br>
Mitigation: Use synthetic or consented data where possible, redact identifying details before import, review generated files before activation, and delete generated directories when finished. <br>
Risk: Generated personas can preserve unhealthy relationship dynamics or misleading character behavior. <br>
Mitigation: Treat the output as entertainment, review the generated persona and memory files, and revise or remove content that encourages harmful or non-consensual use. <br>
Risk: Generated skills may also be copied into an agent skill directory for activation. <br>
Mitigation: Remove both the local simps/{slug} directory and any copied .trae/skills/simp-{slug} directory when the generated character should no longer be available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brother-yang/simp-dog-skill) <br>
- [README_EN.md](artifact/README_EN.md) <br>
- [README.md](artifact/README.md) <br>
- [INSTALL.md](artifact/INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus generated local files and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local simps/{slug}/ memory, persona, metadata, version, and skill files; optional parser scripts summarize chat, social, and photo inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
