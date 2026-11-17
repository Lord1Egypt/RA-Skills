## Description:

Launches RustDesk on Windows, prepares a screenshot directory, captures the full screen, and returns the screenshot path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaohx-star](https://clawhub.ai/user/yaohx-star)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to start RustDesk and capture a Windows desktop screenshot for remote-access setup or support handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshots can expose RustDesk access credentials, passwords, private messages, or other secrets.

Mitigation: Run only in a controlled Windows environment and avoid capturing screens that display secrets or private content.

Risk: The configurable screenshot folder can be cleared before capture.

Mitigation: Set SCREENSHOT_DIR to a dedicated empty folder whose contents can be safely deleted.

Risk: Running with elevated privileges can increase the impact of accidental file deletion or sensitive screen capture.

Mitigation: Use the least-privileged account suitable for the workflow and avoid elevated execution.

## Reference(s):

- [Server-resolved source repository](https://github.com/yaohx-star/rustdesk-screenshot.git)
- [ClawHub skill page](https://clawhub.ai/yaohx-star/skills/rustdesk-screenshot)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Files]

**Output Format:** [JSON status object with a PNG screenshot file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs on Windows with Python and Pillow; supports RUSTDESK_PATH, SCREENSHOT_DIR, and WAIT_SECONDS environment variables.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
