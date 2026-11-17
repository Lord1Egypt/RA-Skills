## Description:

Generates React component templates, with documented support for function components, class components, custom hooks, higher-order components, and TypeScript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to scaffold simple React component code quickly from command examples or shell execution. Review generated output before relying on documented options such as TypeScript or multiple component types.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell script can overwrite files based on an unvalidated component name.

Mitigation: Restrict component names to valid React identifiers, write only inside a chosen output directory, and refuse accidental overwrites.

Risk: The documentation overstates support for TypeScript and multiple component types compared with the current script behavior.

Mitigation: Review generated output and update the documentation or implementation before relying on unsupported options.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshine-del-ux/skills/react-component-generator)
- [Publisher profile](https://clawhub.ai/user/sunshine-del-ux)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash examples and generated JSX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated filenames are based on the supplied component name.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
