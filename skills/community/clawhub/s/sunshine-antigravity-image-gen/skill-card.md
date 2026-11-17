## Description:

Generate images using the internal Google Antigravity API (Gemini 3 Pro Image). High quality, native generation without browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate image files from text prompts through a local Node.js workflow authenticated with a Google Antigravity OAuth profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses local Google OAuth credentials with an internal Antigravity/Google API workflow.

Mitigation: Install only when that workflow is intended, and review the account and project whose token will be used.

Risk: Broad activation rules can let the skill run in more image-generation contexts than intended.

Mitigation: Avoid broad automatic activation and review when the skill should be enabled.

Risk: The output path is unrestricted.

Mitigation: Use controlled output locations and do not let untrusted prompts or agents choose the path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshine-del-ux/skills/sunshine-antigravity-image-gen)
- [Publisher profile](https://clawhub.ai/user/sunshine-del-ux)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [PNG image file with stdout status text and a MEDIA path line]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a prompt; accepts optional output path and aspect ratio.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
