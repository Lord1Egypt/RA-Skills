## Description:

Generate a TPT cover using the AI Studio DinoCover tool and save it locally with the book title as filename.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kakazhang50](https://clawhub.ai/user/kakazhang50)

### License/Terms of Use:


## Use Case:

External creators or operators preparing Teachers Pay Teachers materials use this skill to drive the AI Studio DinoCover tool with local TXT and PNG inputs and save a generated cover image locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The title from the TXT input is used as the output filename and could contain unsafe path characters, reserved Windows names, or a name that overwrites an existing file.

Mitigation: Sanitize titles into safe basenames, reject path separators and reserved Windows names, and check for existing output files before saving.

Risk: The workflow depends on a persisted Google login in the geminibuild browser profile.

Mitigation: Use only a pre-existing trusted browser profile, do not handle login or account changes, and stop for login, MFA, verification, or captcha prompts.

Risk: The browser workflow uploads local reference PNGs to the AI Studio tool.

Mitigation: Run only with trusted local reference images and confirm that uploaded files are appropriate for the target Google account and DinoCover session.

## Reference(s):

- [AI Studio DinoCover Tool](https://aistudio.google.com/apps/drive/1dsPpIhA2HzaacwO16jxddnerC-B64MuC?showPreview=true&showAssistant=true&fullscreenApplet=true)
- [ClawHub Skill Page](https://clawhub.ai/kakazhang50/skills/tpt-generate-cover)

## Skill Output:

**Output Type(s):** [Files]

**Output Format:** [PNG image file saved to a local output folder]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Filename is derived from the first line of the latest TXT input; the generated image is downloaded from the browser tool.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
