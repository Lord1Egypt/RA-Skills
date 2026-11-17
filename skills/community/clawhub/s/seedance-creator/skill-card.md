## Description:

Seedance Creator helps agents write Chinese Seedance 2.0 image and video prompts and, when explicitly used with a logged-in dreamina CLI, run image and video generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chencore](https://clawhub.ai/user/chencore)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and developers use this skill to turn creative briefs or reference media into structured Seedance 2.0 prompts, generation commands, and result-handling guidance for images, videos, image-to-video, and video-extension workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill with a logged-in dreamina CLI account can submit generation jobs and may consume account credits.

Mitigation: Use CLI execution only when intended, review the generated command before running it, and use prompt-only mode when CLI state or account usage is uncertain.

Risk: Image-to-image and image-to-video workflows can upload user-selected local media to the Seedance/dreamina service.

Mitigation: Review file paths before execution and avoid uploading media that contains sensitive, private, or restricted content.

Risk: Broad activation phrases for image and video tasks could trigger the skill when a user only wants general creative guidance.

Mitigation: Prefer explicit /seedance invocation for CLI-backed workflows and confirm intent before executing generation commands.

## Reference(s):

- [dreamina CLI download](https://jimeng.jianying.com/cli)
- [ClawHub skill page](https://clawhub.ai/chencore/skills/seedance-creator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and generated prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dreamina submit IDs, result links, media dimensions, duration, and user-facing cautions about local media uploads.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
