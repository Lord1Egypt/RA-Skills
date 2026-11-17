## Description:

Generate font-based signature images via Signus API and return image files for chat delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[signus-ai](https://clawhub.ai/user/signus-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to request font-based signature images from Signus using a name, first and last name, or initials, then receive generated image files for chat delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe filename or ZIP entry handling can write outside the promised output folder.

Mitigation: Validate path components, enforce output-directory boundaries, and review extracted files before broad deployment.

Risk: ZIP processing or large responses can exhaust local resources.

Mitigation: Add response size limits, extraction limits, and operational monitoring before broad use.

Risk: User-supplied names or initials are sent to Signus and generated signature files are stored locally.

Mitigation: Inform users about the data flow and storage location before using the skill with personal data.

Risk: The bundled ZIP dependency may need maintenance or replacement before broad use.

Mitigation: Update or replace the ZIP dependency as part of deployment review.

## Reference(s):

- [Signus Font Signature on ClawHub](https://clawhub.ai/signus-ai/skills/signus-font-signature)
- [Signus API host](https://api.signus.ai)
- [Publisher profile](https://clawhub.ai/user/signus-ai)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [JSON result with local image file paths, plus chat image delivery by the invoking agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script may create PNG, JPG, JPEG, or WebP files under the local OpenClaw media directory.]

## Skill Version(s):

1.0.1 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
