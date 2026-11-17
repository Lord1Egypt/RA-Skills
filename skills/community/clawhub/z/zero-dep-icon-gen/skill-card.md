## Description:

Generates dependency-free PNG application icons from simple color and symbol specs using a local Python standard-library script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to create simple geometric icons, favicons, and marketplace-ready PNG assets without installing image-processing dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation is primarily in Chinese, which may make options and publishing notes harder for non-Chinese readers to review.

Mitigation: Review the command examples and option tables before running the generator, and translate the documentation when operating in a non-Chinese review workflow.

Risk: The skill includes marketplace-upload guidance, but icon publishing is a separate user-directed action.

Mitigation: Treat generated PNG files as local artifacts until an operator explicitly chooses to upload or publish them through a marketplace process.

Risk: Broad activation wording may cause the skill to be suggested for general icon requests where a richer design workflow is needed.

Mitigation: Use it for simple geometric PNG icons and choose a dedicated design or image-generation workflow for photo-like, branded, or complex illustrative assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oracis/skills/zero-dep-icon-gen)
- [Icon design notes](artifact/references/design-notes.md)
- [Example icon specs](artifact/specs.example.txt)
- [Icon generator script](artifact/scripts/gen_icons.py)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash command examples; script output is PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports individual specs, specs files, custom size and radius values, rotated symbols, shadow variants, and short text glyph icons.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
