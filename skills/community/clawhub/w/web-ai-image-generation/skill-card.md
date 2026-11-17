## Description:

Automates Gemini or ChatGPT web sessions with a reusable browser profile to submit image prompts and save generated images to a local output directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henryczq](https://clawhub.ai/user/henryczq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to generate AI cover images, marketing visuals, and short-video thumbnails through browser-based Gemini or ChatGPT workflows without directly calling image APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent browser profile can retain Gemini or ChatGPT login state.

Mitigation: Use a dedicated isolated profile and remove or rotate it when the workflow no longer needs that login state.

Risk: The automated browser disables key browser protections.

Mitigation: Run it as an unprivileged user in a dedicated environment and review the browser launch flags before use.

Risk: The workflow downloads page-selected URLs to local disk.

Mitigation: Keep the output directory separate from unrelated files and restrict downloads to known image hosts before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/henryczq/skills/web-ai-image-generation)
- [Skill documentation](artifact/SKILL.md)
- [Dependency and installation notes](artifact/DEPENDENCIES.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and local image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved as local JPEG files; browser login state is reused from the configured profile directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
