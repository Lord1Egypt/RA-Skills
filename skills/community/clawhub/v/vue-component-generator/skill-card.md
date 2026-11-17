## Description:

Generates Vue 3 component templates with support for Composition API, Options API, TypeScript, and single-file components.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers and frontend engineers use this skill to create starter Vue 3 single-file components with selected API style, TypeScript, SCSS, props, and emits patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsanitized component names can allow command injection or malformed replacement behavior in the bundled shell script.

Mitigation: Use only trusted component names and reject path separators, traversal sequences, newlines, shell metacharacters, and sed replacement metacharacters before execution.

Risk: The shell script can overwrite arbitrary writable destinations derived from the component name.

Mitigation: Run it in a fixed output directory, validate the final path, and refuse to write when the destination already exists.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshine-del-ux/skills/vue-component-generator)
- [ClawHub publisher profile](https://clawhub.ai/user/sunshine-del-ux)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands]

**Output Format:** [Vue single-file component code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated component filenames and content depend on the provided component name and options.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
