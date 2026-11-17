## Description:

Guides developers in writing and reviewing Rez 3.4.0 package.py definitions, including attributes, dependencies, variants, binding functions, and overrides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to draft, review, and debug Rez package definitions, including runtime and build dependencies, environment setup, and package attributes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copying the illustrative shell-based subprocess example into a package with dynamic command input can be unsafe.

Mitigation: Use subprocess argument lists instead of shell commands when adapting the example, especially with dynamic input.

Risk: Module-level class imports or instances can produce an invalid installed package.py.

Mitigation: Keep class imports and object creation inside functions and validate the installed package before release.

## Reference(s):

- [Rez Package Definition on ClawHub](https://clawhub.ai/loonghao/skills/rez-package-definition)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rez 3.4.0 package.py authoring guidance]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
