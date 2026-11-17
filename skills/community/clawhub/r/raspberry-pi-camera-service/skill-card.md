## Description:

Provides an agent with guidance and code for controlling a Raspberry Pi CSI or USB camera over an HTTP service to capture photos, record H264 or MP4 video, and generate GIFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cld1994](https://clawhub.ai/user/cld1994)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy and operate a Raspberry Pi camera service, then control recording, photo capture, heartbeat-managed sessions, conversion, download, listing, and deletion through a Python client or HTTP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deployed camera service is unauthenticated and listens on all interfaces by default.

Mitigation: Bind the service to localhost or a protected interface, add authentication, and avoid public network exposure.

Risk: The service may run with elevated privileges or as root during deployment.

Mitigation: Use a dedicated non-root service account and review the generated systemd service permissions before enabling it.

Risk: Captured photos and videos are retained on the device and may contain sensitive data.

Mitigation: Restrict filesystem and network access, set retention expectations, and delete media files when they are no longer needed.

Risk: The installer creates a Python environment and installs dependencies on the target system.

Mitigation: Review the dependency installation behavior and run deployment only on a trusted Raspberry Pi.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cld1994/skills/raspberry-pi-camera-service)
- [CameraClient usage guide](references/client_usage.md)
- [Camera service deployment guide](references/deploy_service.md)
- [Raspberry Pi camera HTTP service design](references/design.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or manage camera media files through the deployed service, including JPEG, H264, MP4, and GIF outputs.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
