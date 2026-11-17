## Description:

Generate PPT decks from prompts/block XML while preserving corporate brand style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phil-osophy-42](https://clawhub.ai/user/phil-osophy-42)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users use this skill to generate branded PowerPoint decks from structured XML or prompts while reusing an existing corporate PPT template.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted template_file or output_filename values can read templates or overwrite files outside the intended workspace.

Mitigation: Use only trusted template_file and output_filename values, reject absolute paths and ../ components, and run the skill in a restricted workspace.

Risk: Dependency drift can change runtime behavior before broad use.

Mitigation: Pin and review dependencies, including python-pptx, before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phil-osophy-42/skills/slug)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [PPTX file with a status object containing output_path, slide_count, and message fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python-pptx and a local PPT template file.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and manifest.yaml; SKILL.md frontmatter lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
