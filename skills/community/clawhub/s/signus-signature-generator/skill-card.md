## Description:

Generate signature images via the Signus API and return image files for chat delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[signus-ai](https://clawhub.ai/user/signus-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to generate signature images from a provided name, first and last name, or initials through the Signus API and return generated image files for chat delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signature identity data is sent to api.signus.ai.

Mitigation: Install only when users are comfortable sharing that data with Signus, and disclose this network dependency before use.

Risk: Generated signature images are stored locally and the evidence does not define cleanup or retention behavior.

Mitigation: Define retention and cleanup expectations for generated files under ~/.openclaw/media/signatures-font/.

Risk: Evidence security guidance flags weak file-writing and ZIP extraction safeguards.

Mitigation: Review output-directory containment, sanitize path components, avoid remote IDs as filenames, and add network and archive size limits before broad deployment.

Risk: The dependency list uses adm-zip, which evidence guidance says to update or replace.

Mitigation: Update or replace adm-zip and verify archive handling before production rollout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/signus-ai/skills/signus-signature-generator)
- [Signus API host](https://api.signus.ai)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [JSON metadata with local image file paths and chat-delivered signature images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated image files under ~/.openclaw/media/signatures-font/ and may return a count-limited set of signatures.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
