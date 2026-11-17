## Description:

Process text templates with variable substitution. Use for generating dynamic content from template files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to process text templates with variable substitution and to generate starter project or content files from reusable templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled scaffold generator can write or overwrite files outside the intended output directory.

Mitigation: Run the skill only in a controlled project directory, avoid untrusted template names or output paths, and inspect generated files before executing them.

Risk: The release has a suspicious security verdict because the artifact includes scaffold-generation behavior beyond simple text-template processing.

Mitigation: Review the skill before installing and confirm that scaffold generation is acceptable for the intended use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/template-tool)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Shell commands, Configuration]

**Output Format:** [Plain text, Markdown, code/configuration file contents, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or overwrite files when scaffold-generation behavior is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
