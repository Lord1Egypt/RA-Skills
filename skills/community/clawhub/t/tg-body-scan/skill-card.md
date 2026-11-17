## Description:

Runs a Telegram body-scan workflow that validates inputs and consent, submits a video to the AnthroVision bridge, polls status, and returns structured body measurements and waist-to-hip ratio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External Telegram users and agents use this skill to collect consent, submit a single-person body-scan video, monitor processing status, and return structured body measurements for fitness tracking, body measurement, sports performance analysis, or body composition change monitoring. It is not intended for medical diagnosis, minors, non-consensual videos, or multi-person videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends intimate body-scan videos and measurements to the AnthroVision bridge without clear retention, deletion, logging, or privacy details in the evidence.

Mitigation: Use only after confirming the bridge provider's privacy, retention, deletion, and logging practices, and require explicit consent before processing any real-person video.

Risk: The artifact declares read, write, and exec authority even though the documented workflow should not need shell command access.

Mitigation: Prefer a release with exec removed, or run the skill in a constrained agent profile that denies shell access and limits file permissions to what the workflow actually needs.

Risk: Body measurement output can be mistaken for health or medical assessment.

Mitigation: Keep responses limited to measurements and waist-to-hip ratio, and preserve the artifact's restrictions against medical diagnosis, minors, non-consensual videos, and multi-person scans.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/tg-body-scan)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with structured scan status and measurement fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scan_id, status, measurements, waist-to-hip ratio, timeout prompts, and deterministic formatting that avoids passing through untrusted upstream strings.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
