## Description:

Extends an existing video clip, or replaces its ending, by extracting a local frame, using it as the first frame for a new Ofox-generated segment, and joining the segment back onto the source clip.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofoxai](https://clawhub.ai/user/ofoxai)

### License/Terms of Use:

MIT-0

## Use Case:

Agents, developers, and video creators use this skill when a user has an existing clip and wants to extend it, add another shot, or replace the ending from a chosen frame. It helps produce local extraction and join commands, Ofox generation steps, and guidance for pricing and approval before paid video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid Ofox generation can incur charges.

Mitigation: Use dry-run pricing first and run approved generation commands only after the cost is shown to and accepted by the user.

Risk: A selected frame and prompt are sent to Ofox for generation.

Mitigation: Use only footage the user is authorized to process and disclose the upload before submitting a paid job.

Risk: The workflow depends on the companion ofox-video-core skill and local tools.

Mitigation: Review or install ofox-video-core 2.0.0 or newer from the same source, check curl, jq, ffmpeg, and OFOX_API_KEY before paid execution, and keep the API key scoped appropriately.

Risk: Joining the generated segment without normalization can produce silent or inconsistent video output.

Mitigation: Follow the documented ffmpeg normalization and verification steps, and explicitly choose the audio hand-off before delivering the final video.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ofoxai/skills/video-extend-edit)
- [Skill homepage](https://github.com/ofoxai/skills/tree/main/skills/video-extend-edit)
- [Ofox API keys](https://app.ofox.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local ffmpeg commands, Ofox dry-run and approved generation commands, dependency checks, and post-generation verification steps.]

## Skill Version(s):

2.0.0 (source: server release evidence, frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
