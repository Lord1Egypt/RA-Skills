## Description: <br>
Continuous self-improvement through structured reflection and memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hopyky](https://clawhub.ai/user/hopyky) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to prompt periodic self-review, read recent lessons, and log fixes into local reflection memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reflection logs create persistent local memory that could capture secrets, private user data, tokens, or sensitive project details if an agent records them. <br>
Mitigation: Do not log sensitive data; review the configured memory file regularly and remove entries that should not persist. <br>
Risk: The README installation flow references an external CLI that was not included in the reviewed package. <br>
Mitigation: Inspect the external CLI source before symlinking or running it, and only install it from a trusted source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hopyky/self-reflection) <br>
- [README](artifact/README.md) <br>
- [Skill manifest](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and reads persistent local reflection memory according to the user's configuration.] <br>

## Skill Version(s): <br>
1.1.1 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
