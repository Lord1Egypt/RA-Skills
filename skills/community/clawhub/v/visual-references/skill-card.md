## Description:

Searches and downloads visual reference images from Pexels to support style, mood, composition, and color-palette inspiration before generating visual assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vdkroon](https://clawhub.ai/user/vdkroon)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, developers, and creative agents use this skill when a visual brief is ambiguous or style-driven and Pexels reference images can inform image or video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script deletes matching ref_* files and refs_meta.json in the selected output folder before downloading results.

Mitigation: Run it only with a dedicated temporary output directory such as /tmp/visual-refs; do not point --output at a working project or home directory.

Risk: The skill requires a PEXELS_API_KEY and calls the Pexels API.

Mitigation: Use a dedicated Pexels API key and avoid exposing the key in prompts, logs, shared shell history, or committed configuration.

Risk: The release metadata declares an unused unpinned requests dependency.

Mitigation: Review dependency requirements before installation and remove or pin requests if it remains necessary.

## Reference(s):

- [Visual References ClawHub Release](https://clawhub.ai/vdkroon/skills/visual-references)
- [Pexels API Documentation](https://pexels.com/api)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Text, Guidance]

**Output Format:** [Downloaded JPG files, refs_meta.json, and stdout attribution text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PEXELS_API_KEY; default output directory is /tmp/visual-refs; supports count, orientation, and list-only options.]

## Skill Version(s):

2.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
