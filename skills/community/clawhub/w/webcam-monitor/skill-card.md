## Description:

Webcam motion detection and monitoring system for WSL2 with USB/IP passthrough.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jadegaul](https://clawhub.ai/user/jadegaul)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure webcam motion detection in WSL2, capture snapshots on motion, monitor new images, and optionally preview the live camera stream in a browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The live webcam preview server can expose camera output on all network interfaces without authentication.

Mitigation: Bind the preview server to 127.0.0.1 or add authentication and network access controls before running it.

Risk: The setup guidance recommends broad camera device permissions.

Mitigation: Avoid chmod 666 for /dev/video0; use least-privilege device access such as group membership or narrower permissions.

Risk: Captured snapshots and person-identification memory entries may contain sensitive personal information.

Mitigation: Store snapshots in a protected location, review retention settings, and limit identifying memory entries to information that is necessary and consented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jadegaul/skills/webcam-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python code references, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local webcam snapshots, log files, queue files, and a live preview server when the included scripts are run.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
