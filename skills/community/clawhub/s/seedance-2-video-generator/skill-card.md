## Description:

Generate Werydance 2.0 videos through WeryAI for text-to-video, image-to-video, multi-image video, first-frame/last-frame transitions, and mixed image, video, audio, and text references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fwwdn](https://clawhub.ai/user/fwwdn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to prepare prompts and parameters, confirm paid WeryAI video-generation requests, run the packaged Node.js CLI, and return task status or playable video URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Endpoint overrides can send the WeryAI API key and selected media to an untrusted server.

Mitigation: Use only official WeryAI endpoints and keep WERYAI_BASE_URL and WERYAI_MODELS_BASE_URL unset unless the destination is fully trusted and uses HTTPS.

Risk: Local file paths are uploaded with the configured WeryAI API key during real generation runs.

Mitigation: Prefer public HTTPS media URLs and use dry runs to review uploadPreview before consenting to any local file upload.

## Reference(s):

- [Werydance 2.0 Prompt Optimization](references/seedance-prompt-optimization.md)
- [ClawHub Skill Page](https://clawhub.ai/fwwdn/skills/seedance-2-video-generator)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns WeryAI task identifiers, polling status, errors, and video URLs when generation succeeds.]

## Skill Version(s):

0.1.2 (source: server release metadata; artifact frontmatter version 1.0.1 differs)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
