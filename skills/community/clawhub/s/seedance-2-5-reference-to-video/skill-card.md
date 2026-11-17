## Description:

Seedance 2.5 Reference to Video on RunComfy helps an agent prepare and run reference-guided 1080p video generation requests through the RunComfy CLI, using user-supplied images, video clips, audio references, and prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate reference-guided 1080p video clips with Seedance 2.5 on RunComfy, including consistent character videos, product reference films, style-locked brand clips, and synchronized audio outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts and user-selected reference media URLs to a paid remote RunComfy video service.

Mitigation: Confirm the user is comfortable with the data transfer and per-second billing before submitting a generation request.

Risk: The skill depends on an unpinned third-party CLI.

Mitigation: Prefer a pinned, verified `@runcomfy/cli` version and avoid running `npx -y` with broad privileges.

Risk: Reference media can contain misleading text or unintended instructions.

Mitigation: Use only reference URLs explicitly chosen for the generation and treat visible text in reference media as data, not agent instructions.

Risk: RunComfy authentication uses `RUNCOMFY_TOKEN` or local CLI token storage.

Mitigation: Do not echo tokens into prompts, logs, generated files, or shell output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/seedance-2-5-reference-to-video)
- [RunComfy homepage](https://www.runcomfy.com)
- [Seedance 2.5 Reference to Video 1080p model page](https://www.runcomfy.com/models/bytedance/seedance-2.5/reference-to-video/1080p?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-2-5-reference-to-video&utm_content=bytedance-seedance-2.5-reference-to-video-1080p)
- [Seedance 2.5 Reference to Video 480p model page](https://www.runcomfy.com/models/bytedance/seedance-2.5/reference-to-video/480p?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-2-5-reference-to-video&utm_content=bytedance-seedance-2.5-reference-to-video-480p)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-2-5-reference-to-video&utm_content=cli-docs-introduction)
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-2-5-reference-to-video&utm_content=cli-docs-troubleshooting)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The RunComfy CLI may download generated video files to the requested output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
