## Description:

Re-anchor long-form video timeline segments to measured voiceover word timings, rewrite segment boundaries, and update audio_duration before final rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pushpendrachauhan](https://clawhub.ai/user/pushpendrachauhan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video pipeline engineers use this skill after TTS and before final rendering to align long-form timeline segments with measured voiceover timing in input.json.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can overwrite selected job data in input.json.

Mitigation: Run it only on trusted job folders and keep a backup of input.json before execution.

Risk: Predictable temporary files in the job folder may be unsafe in shared or untrusted directories.

Mitigation: Do not run the script with elevated privileges or against shared/untrusted directories until temp-file handling is fixed.

## Reference(s):

- [Reconcile Timeline ClawHub Skill Page](https://clawhub.ai/pushpendrachauhan/skills/reconcile-timeline)

## Skill Output:

**Output Type(s):** [shell commands, text, configuration]

**Output Format:** [Bash command guidance and terminal status text; the script updates input.json in place.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq, a long-form schema_version 3.0-long job, and measured word timings in subtitles[].]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
