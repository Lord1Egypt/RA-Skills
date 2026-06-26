## Description: <br>
Guides a user through a structured interview to define requirements, collect supporting materials, and produce a complete reusable Skill package. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[irenerachel](https://clawhub.ai/user/irenerachel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create a new Skill by answering guided interview questions instead of writing the Skill package structure directly. It is intended for new Skill creation, not small edits to an existing complete SKILL.md or one-off prompt requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Skill packages can include user-provided files, so sensitive or proprietary material could be bundled unintentionally. <br>
Mitigation: Review the file list before delivery and exclude credentials, private keys, sensitive personal data, or proprietary documents unless they are intentionally part of the Skill package. <br>
Risk: The skill can write folders or create a zip archive as part of delivery, so an incorrect destination could place files somewhere unintended. <br>
Mitigation: Confirm the destination path or archive name before writing and review the completed package contents. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown conversation output plus generated Skill package files or a zip archive when the runtime supports packaging] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create SKILL.md, references, examples, scripts, assets, placeholder README files, and test prompts based on the interview results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
