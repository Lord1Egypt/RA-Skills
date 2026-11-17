## Description:

Captures full-screen Windows screenshots with a mouse-position marker and runs local OCR through the Windows native OCR engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a770438678](https://clawhub.ai/user/a770438678)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to capture Windows screen state, mark the cursor location, and extract text from screenshots without sending data to an external OCR service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full-screen capture can save visible passwords, tokens, private messages, or confidential documents to disk.

Mitigation: Run only when sensitive content is hidden, store captures in an appropriate folder, and delete screenshots and OCR output when no longer needed.

Risk: The scripts use a fixed Windows output path and a hard-coded OCR input path.

Mitigation: Review and change the paths before execution so files are saved and read from the intended location.

Risk: Unpinned Python dependencies may resolve to unexpected package versions.

Mitigation: Install in a non-admin virtual environment and pin dependency versions before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a770438678/skills/windows-screenshot-ocr)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python commands and local file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local PNG screenshots and UTF-8 OCR text files on Windows; no network upload behavior was identified in the security evidence.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
