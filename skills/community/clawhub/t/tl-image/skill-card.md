## Description:

Generates and edits images through TensorsLab AI models for text-to-image, image-to-image, avatar, object erasure, watermark removal, face replacement, and general image editing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bob5-tensorslab](https://clawhub.ai/user/bob5-tensorslab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create and transform images with TensorsLab models, including avatar generation, object erasure, watermark removal, face replacement, and general edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected source images are sent to TensorsLab for processing.

Mitigation: Avoid confidential, regulated, copyrighted, or identity-sensitive content unless provider terms and user permissions have been reviewed.

Risk: Watermark removal and face replacement workflows can create rights, consent, or impersonation concerns.

Mitigation: Confirm that the user has permission for the edit and that the intended use is appropriate before processing.

Risk: Downloaded outputs may be written to the local working directory or a user-selected output directory.

Mitigation: Run the script in a limited working directory and use an explicit output directory until filename and download validation are improved.

## Reference(s):

- [TensorsLab Image Skill Release](https://clawhub.ai/bob5-tensorslab/skills/tl-image)
- [TensorsLab Publisher Profile](https://clawhub.ai/user/bob5-tensorslab)
- [TensorsLab Image API Reference](references/api_reference.md)
- [TensorsLab Image Generation Scenarios](references/scenarios.md)
- [TensorsLab API](https://api.tensorslab.com)
- [TensorsLab Console](https://tensorai.tensorslab.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands and local image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TENSORSLAB_API_KEY; generated images are saved under tensorslab_output or a user-selected output directory.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
