## Description: <br>
Capture screenshots on Windows using mss and Pillow, including full-screen, region, and multi-monitor capture with output as a PIL Image, PNG file, or base64 string. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunrddd-a11y](https://clawhub.ai/user/sunrddd-a11y) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users use this skill to capture local screen content, inspect monitor dimensions, save screenshots, or prepare base64 image payloads for vision workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots may capture private windows, credentials, customer data, or other sensitive local content. <br>
Mitigation: Review the visible screen before capture, prefer region capture over full-screen capture, and close or crop out private windows. <br>
Risk: Saved screenshots and base64 image strings may persist sensitive data or be sent to external APIs. <br>
Mitigation: Delete saved screenshots when no longer needed and send base64 output externally only after reviewing the image contents. <br>


## Reference(s): <br>
- [Screenshot Capture API Reference](reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/sunrddd-a11y/screenshot-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Files, Configuration] <br>
**Output Format:** [Markdown guidance, Python examples, shell commands, PNG or JPEG image files, and base64 strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can output monitor information as JSON through the CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
