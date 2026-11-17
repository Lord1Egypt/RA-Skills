## Description:

Generate QR codes from URLs or text using a pre-built Python script with qrcode library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whubbt](https://clawhub.ai/user/whubbt)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to generate PNG QR codes from URLs or arbitrary text through a local Python script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create directories and write a PNG file to a user-selected path.

Mitigation: Choose an output path that will not overwrite important files and review paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whubbt/skills/qrcode-gen-yn)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with bash command examples; the script writes a PNG image file and prints the generated file path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a PNG file to a caller-selected path; default QR settings use 10-pixel boxes and a 4-box border.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
