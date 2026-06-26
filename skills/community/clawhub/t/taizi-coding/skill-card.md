## Description: <br>
Coding style memory that adapts to your preferences, conventions, and patterns for consistent coding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fresh3](https://clawhub.ai/user/fresh3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to remember explicitly confirmed coding preferences, apply them to future code output, and support user requests to show or forget stored preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confirmed coding preferences are retained locally and may continue influencing future coding responses. <br>
Mitigation: Store preferences only after explicit confirmation and review or delete ~/coding/memory.md to clear retained preferences. <br>
Risk: Supporting criteria text is slightly inconsistent about where updates should be written. <br>
Mitigation: Follow SKILL.md's explicit rules: store preferences in ~/coding/memory.md only after confirmation and do not modify the skill file itself. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fresh3/taizi-coding) <br>
- [Skill homepage](https://clawic.com/skills/coding) <br>
- [Criteria for Code Preferences](artifact/criteria.md) <br>
- [Code Dimensions to Detect](artifact/dimensions.md) <br>
- [Memory Templates](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and compact preference entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores confirmed preferences in local files under ~/coding/ with a 100-line active memory limit.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter is 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
