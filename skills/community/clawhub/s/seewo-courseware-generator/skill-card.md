## Description:

Generate multi-page, editable Seewo Whiteboard courseware files in the native .enbx format from lesson topics, outlines, or free-form teaching material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[insistandtry](https://clawhub.ai/user/insistandtry)

### License/Terms of Use:

MIT-0

## Use Case:

External educators, instructional designers, and agents assisting them use this skill to turn lesson content into native, editable Seewo Whiteboard courseware. It is useful when the deliverable must be an .enbx file rather than a PPTX or PDF.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can package local image files referenced by a courseware specification.

Mitigation: Use a dedicated trusted image folder and avoid image paths supplied by untrusted users.

Risk: The security summary notes missing input-size limits.

Mitigation: Run generation and validation with normal sandbox and resource limits, especially for large lesson specs.

Risk: Attacker-supplied JSON specs or ENBX files may create unsafe or misleading outputs.

Mitigation: Review lesson specs before generation, validate outputs, and use fresh output paths.

## Reference(s):

- [ENBX Courseware Format Reference](references/enbx_format.md)
- [ClawHub Skill Page](https://clawhub.ai/insistandtry/skills/seewo-courseware-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON specifications, shell commands, and generated .enbx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces native Seewo Whiteboard .enbx courseware and validation guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
