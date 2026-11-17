## Description:

Generate and edit images using TensorsLab's AI models, including text-to-image, image-to-image, avatar generation, watermark removal, object erasure, face replacement, prompt enhancement, progress tracking, and local file saving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bob5-tensorslab](https://clawhub.ai/user/bob5-tensorslab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate new images, transform source images, and run guided image-editing workflows through the TensorsLab API. The skill is useful when an agent needs to prepare prompts, call the image service, monitor asynchronous jobs, and save generated image files locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user prompts and source images to TensorsLab.

Mitigation: Use it only with prompts and images approved for third-party processing, and avoid confidential or personal images unless policy allows that use.

Risk: Watermark-removal and face-replacement workflows can be misused.

Mitigation: Run these workflows only for clearly authorized, consensual cases and review requests before execution.

Risk: The bundled downloader has validation weaknesses around task IDs, download hosts, redirects, and response size.

Mitigation: Harden the downloader before sensitive or routine deployment by validating task IDs, restricting download hosts, disabling unsafe redirects, and limiting download size.

## Reference(s):

- [TensorsLab Image API Reference](references/api_reference.md)
- [TensorsLab Image Generation Scenarios](references/scenarios.md)
- [TensorsLab Console](https://tensorai.tensorslab.com/)
- [ClawHub Skill Page](https://clawhub.ai/bob5-tensorslab/skills/tensorslab-image)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Downloaded image files with Markdown-style status messages and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved to tensorslab_output by default or to a user-specified output directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
