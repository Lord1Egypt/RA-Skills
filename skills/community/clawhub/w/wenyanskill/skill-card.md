## Description:

WenYan converts agent replies into eight configurable classical Chinese styles using JSON style definitions and a Python validation and scoring engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pondsi](https://clawhub.ai/user/pondsi)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use WenYan to make agents answer in configurable classical Chinese styles while preserving technical text such as commands, paths, and code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell-based validation examples may encourage unsafe command construction if user text is interpolated directly.

Mitigation: Run validation in a sandboxed or scoped workspace and pass text safely instead of copying echo pipelines literally.

Risk: Persistent style state can change future agent behavior beyond the current request.

Mitigation: Restrict style IDs to known values and require clear user intent or confirmation before persistent mode changes.

Risk: Generated prompts can affect all replies if installed in account-wide or app-wide instructions.

Mitigation: Install generated prompts only in the intended agent, project, or session scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pondsi/skills/wenyanskill)
- [README](artifact/README.md)
- [Agent integration guide](artifact/assets/agents.md)
- [Style comparison reference](artifact/assets/style-comparison.md)
- [Style examples](artifact/assets/examples.md)
- [Style configuration files](artifact/references/styles/)
- [Shared address and taboo-word references](artifact/references/shared/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Classical Chinese styled prose, Markdown guidance, JSON-backed style configuration, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports eight styles and three intensity levels; validation and scoring require python3.]

## Skill Version(s):

1.0.0 (source: frontmatter, manifest.json, CHANGELOG, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
