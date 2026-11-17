## Description:

Control MindReset Dot Quote/0 through a local Node.js CLI that calls Dot Developer Platform APIs for device status, content listing, text updates, image updates, and content switching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangguangzhou](https://clawhub.ai/user/yangguangzhou)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate a MindReset Dot Quote/0 device from an agent session, including checking device state, pushing text or PNG image content, switching content, and troubleshooting Dot Open API setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real Dot API credentials can be exposed if passed directly as command-line arguments or stored in shell history.

Mitigation: Prefer short-lived environment variables or a secret manager, avoid persisting credentials in shell profiles unless explicitly approved, and rotate any key that may have been exposed.

Risk: The skill can modify text or image content displayed on authorized Dot devices.

Mitigation: Confirm the target DOT_DEVICE_ID and review text or image content before running update or refresh commands.

Risk: Local PNG files provided with --imageFile are read and uploaded to the Dot API.

Mitigation: Use only intended non-sensitive PNG files and avoid passing paths that may contain confidential images or exported documents.

## Reference(s):

- [ClawHub Quote/0 Skill Page](https://clawhub.ai/yangguangzhou/skills/quote0)
- [Dot Open API Documentation](https://dot.mindreset.tech/docs/service/open)
- [Dot API Key Documentation](https://dot.mindreset.tech/docs/service/open/get_api)
- [Dot Device ID Documentation](https://dot.mindreset.tech/docs/service/open/get_device_id)
- [Dot Device List API](https://dot.mindreset.tech/docs/service/open/list_devices_api)
- [Dot Device Status API](https://dot.mindreset.tech/docs/service/open/device_status_api)
- [Dot Device Next API](https://dot.mindreset.tech/docs/service/open/device_next_api)
- [Dot Device Content List API](https://dot.mindreset.tech/docs/service/open/list_device_tasks_api)
- [Dot Text API](https://dot.mindreset.tech/docs/service/open/text_api)
- [Dot Image API](https://dot.mindreset.tech/docs/service/open/image_api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Node.js and requires DOT_API_KEY; device actions also require DOT_DEVICE_ID.]

## Skill Version(s):

1.0.4 (source: package.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
