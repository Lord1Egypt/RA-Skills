## Description:

Connect to Tapo cameras, verify local access, capture snapshots, and inspect frames with local-first RTSP workflows and safe fallbacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to work with their own Tapo cameras on a trusted local network, validate reachability and authentication, capture a single local still image, and troubleshoot RTSP, ONVIF, or local API fallback paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can send camera authentication material to a supplied host outside the intended local camera boundary.

Mitigation: Verify the camera IP or hostname before running the helper, keep the workflow on the trusted LAN, and avoid public or ambiguous hostnames.

Risk: Credential-bearing RTSP URLs can expose camera secrets if printed or reused casually.

Mitigation: Keep credentials in short-lived environment variables or a secret manager, and avoid --show-rtsp unless the credential-bearing URL is needed for another local tool.

Risk: Saved frames may contain sensitive private imagery.

Mitigation: Capture only user-approved still images to explicit local paths and do not upload frames to external services by default.

## Reference(s):

- [Tapo Camera ClawHub page](https://clawhub.ai/ivangdavila/skills/tapo-camera)
- [Tapo Camera homepage](https://clawic.com/skills/tapo-camera)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration notes, and local helper usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local file paths for user-approved captures and notes; does not upload frames by default.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
