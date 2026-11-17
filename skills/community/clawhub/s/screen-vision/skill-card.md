## Description:

macOS screen OCR and click automation via Apple Vision and ScreenCaptureKit for capturing screens or windows, extracting text with coordinates, finding text, and clicking it from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackyun1024](https://clawhub.ai/user/jackyun1024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation-focused users use this skill to inspect visible macOS screens or app windows, check whether text is present, wait for text to appear, and trigger text-based clicks from an agent terminal session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can capture visible screen contents, including sensitive information.

Mitigation: Use it only when Screen Recording access is appropriate, avoid running commands while sensitive information is visible, and scope capture with --app or --region when possible.

Risk: The tap command can perform real mouse clicks based on OCR results.

Mitigation: Review the target text and visible UI before clicking, prefer scoped commands, and use retries only when the destination is stable.

Risk: The setup script installs external software from Homebrew or GitHub release assets.

Mitigation: Run automatic setup only after trusting or independently verifying the upstream Homebrew tap, GitHub release asset, or source build path.

## Reference(s):

- [Screen Vision source project](https://github.com/jackyun1024/mac-screen-vision)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON or human-readable command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce OCR text, screen coordinates, confidence values, found status, and click status; commands require macOS Screen Recording permission.]

## Skill Version(s):

1.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
