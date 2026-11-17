## Description:

AI-powered photo editing and restoration skill - smart object removal, background removal, old photo restoration, and basic edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoxh](https://clawhub.ai/user/guoxh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to select and run photo-editing workflows, including deterministic resizing, cropping, color adjustment, background removal, object removal, restoration, scene replacement, and portrait retouching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected photos and metadata may be processed by external services for AI editing features.

Mitigation: Strip EXIF and location metadata before sensitive cloud AI edits, and use local deterministic tools when external processing is not acceptable.

Risk: Large reference images may be sent through a user-configured Cloudflare R2 worker when upload support is enabled.

Mitigation: Enable R2 upload only with a trusted worker and token, and review worker access controls before use.

Risk: Unpinned Python dependencies or optional image tools can change behavior across environments.

Mitigation: Pin dependencies in the deployment environment and test critical edits before batch use.

Risk: Image editing commands write output files and can overwrite important files if paths are chosen poorly.

Mitigation: Use distinct output paths and keep backups of source images before running destructive or batch operations.

## Reference(s):

- [Smart Photo Editor on ClawHub](https://clawhub.ai/guoxh/skills/smart-photo-editor)
- [VolcEngine Ark Seedream setup guide](https://www.volcengine.com/docs/82379/2375486)
- [Cloudflare R2 documentation](https://developers.cloudflare.com/r2/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, CLI arguments, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce edited image files through local scripts and optional external AI or upload services when configured.]

## Skill Version(s):

1.5.2 (source: server release metadata; artifact metadata reports 1.5.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
