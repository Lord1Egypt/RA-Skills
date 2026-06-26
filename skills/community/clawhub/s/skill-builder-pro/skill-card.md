## Description: <br>
Automated Skill development tool that takes a prompt and feature description, then helps an agent complete ClawHub skill creation, testing, and publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bustes01](https://clawhub.ai/user/bustes01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to turn a requested capability into a ClawHub-ready skill directory, SKILL.md, validation flow, and publish command sequence. It is intended for normal ClawHub skill releases where the user reviews the generated skill before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated skills can accidentally include credentials, personal information, local paths, or private implementation details. <br>
Mitigation: Review each generated skill before publishing and run the documented privacy scan; keep credentials in environment variables rather than SKILL.md. <br>
Risk: The skill can create local skill files and use an authenticated ClawHub CLI session to publish releases. <br>
Mitigation: Install only when comfortable with that workflow, inspect generated files, and publish only after explicit confirmation. <br>


## Reference(s): <br>
- [ClawHub skill homepage](https://clawhub.ai/BusTes01/skill-builder-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with YAML frontmatter examples and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local skill files and publish through the ClawHub CLI after user confirmation.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
