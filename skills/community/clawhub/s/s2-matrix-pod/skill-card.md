## Description:

Assigns a deterministic local habitat and visual avatar to an OpenClaw agent, writes a local JSON state file, and emits Markdown with remote image URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users and developers use this skill to give an OpenClaw agent a repeatable local pod identity, avatar, coordinates, and shareable Markdown profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes a visible JSON state file in the current working directory.

Mitigation: Run it only in a workspace where creating an s2_matrix_data directory and pod state file is acceptable.

Risk: Rendered Markdown can load remote images from spacesq.org when pasted into a Markdown viewer.

Mitigation: Use Markdown viewers that sanitize raw HTML or block remote resources when remote image loading is not desired.

Risk: Untrusted agent names may be embedded into generated Markdown-like output.

Mitigation: Avoid untrusted HTML-like input for the agent name before copying output into Markdown viewers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-matrix-pod)
- [Space2.world](https://space2.world)
- [Space2 image host](https://spacesq.org)

## Skill Output:

**Output Type(s):** [text, markdown, files]

**Output Format:** [Console text containing Markdown plus a local JSON state file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates an s2_matrix_data directory in the current working directory and writes a visible pod state JSON file.]

## Skill Version(s):

1.0.0 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
