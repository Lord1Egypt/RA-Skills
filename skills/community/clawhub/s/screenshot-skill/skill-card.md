## Description:

Capture screenshots on Windows using mss and Pillow, including full-screen, region, and multi-monitor capture with output as a PIL Image, PNG or JPEG file, or base64 string.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunrddd-a11y](https://clawhub.ai/user/sunrddd-a11y)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to capture Windows desktop screenshots, screen metadata, selected regions, or base64 image data for automation and vision-model workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can capture passwords, chats, customer data, financial data, internal documents, or other visible desktop content.

Mitigation: Close sensitive windows before capture and prefer region capture to limit the visible area.

Risk: Base64 screenshot output can expose screen contents if printed to logs or copied into unintended systems.

Mitigation: Avoid logging base64 screenshots and send image data only to intended, approved vision workflows.

Risk: The skill depends on local screenshot libraries that run with access to the user's desktop session.

Mitigation: Install in a virtual environment with reviewed, pinned versions of mss and Pillow.

## Reference(s):

- [Screenshot Capture API Reference](artifact/reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; the included script can produce image files, PIL Image objects, JSON monitor information, or base64 image strings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshot outputs may contain sensitive desktop data and should be reviewed before saving, logging, or sending to vision APIs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
