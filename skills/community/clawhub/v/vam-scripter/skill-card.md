## Description:

VAM Scripter provides documentation and example scripts for using the JavaScript-inspired Virt-A-Mate Scripter environment to automate poses, animations, audio, interactions, scene access, and state handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nffdasilva](https://clawhub.ai/user/nffdasilva)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Virt-A-Mate creators use this skill as a scripting reference and example library for building scene automation, interaction detection, animation, audio triggers, keybindings, player proximity responses, and scene-local state persistence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example scripts that use scene-local file operations can save, overwrite, or delete scene files.

Mitigation: Review any use of fs.writeSceneFileSync or fs.unlinkSceneFileSync before copying examples into VAM, and test persistence behavior with disposable scene data first.

Risk: Example scripts depend on scene-specific atom names, audio clips, and keybinding names.

Mitigation: Verify atom names, audio clip references, and keybindings match the target scene before running copied scripts.

## Reference(s):

- [VAM Scripter Skill Page](https://clawhub.ai/nffdasilva/skills/vam-scripter)
- [Module API Reference](references/module-api.md)
- [Common Patterns and Examples](references/common-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown documentation with JavaScript-like code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reusable example scripts for VAM Scripter scenes.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
