## Description:

Aligns two or more video or audio recordings of the same event to a shared timeline and writes lightweight `.sync.json` sidecars without re-encoding originals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianshuo](https://clawhub.ai/user/jianshuo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media engineers use this skill to compute timeline offsets for multi-camera or separate-audio recordings and produce sidecar metadata that downstream tools can apply with ffmpeg or editing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-selected media files and runs local ffmpeg/ffprobe on them.

Mitigation: Use it only on media the user intends to process and rely on trusted local ffmpeg/ffprobe installations.

Risk: The skill creates or updates `.sync.json` files beside the selected recordings.

Mitigation: Run it in the intended project directory and review or back up existing sidecars before replacing them.

Risk: The documentation contains a stale contradictory line about `_synced.MOV` output.

Mitigation: Treat `.sync.json` sidecars as the authoritative output and verify generated metadata before downstream editing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jianshuo/skills/wjs-syncing-multicam)
- [Skill source documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and `.sync.json` sidecar files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one sync sidecar per input media file; originals are intended to remain unchanged.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
