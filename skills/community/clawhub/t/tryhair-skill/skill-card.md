## Description:

AI hairstyle try-on and face-shape analysis for user-provided photos, requiring a TryHair UID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guokai-01](https://clawhub.ai/user/guokai-01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit a face photo and TryHair UID for face-shape analysis or hairstyle preview generation. The agent presents returned face-shape metrics, hairstyle recommendations, status messages, and generated image links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Face photos and a TryHair UID are sent to tryhair.ai.

Mitigation: Run the skill only on explicit user intent, confirm the photo and UID before processing, and install only when this external processing is acceptable.

Risk: Security evidence flags broad automatic triggers, URL image fetching, and local output file writes.

Mitigation: Use explicit commands, avoid untrusted image_url inputs, review requested actions before execution, and delete generated files from output/ when done.

## Reference(s):

- [TryHair AI homepage](https://tryhair.ai)
- [ClawHub TryHair AI skill listing](https://clawhub.ai/guokai-01/skills/tryhair-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [JSON from the script, usually presented by the agent as Markdown text or image links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided TryHair UID and a clear face photo; generated images may remain in output/ until deleted.]

## Skill Version(s):

0.1.4 (source: server release evidence and publish.sh)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
