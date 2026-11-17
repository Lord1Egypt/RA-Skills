## Description:

Generates 1080P image-to-video clips from first and last frame images using the Volcano Engine Jimeng AI API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdt328606](https://clawhub.ai/user/sdt328606)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to submit first-frame and last-frame image-to-video generation jobs to Jimeng, poll for results, and save the generated video file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and first/last frame images are sent to an external Volcengine API under the user's VOLC credentials.

Mitigation: Use only approved content and credentials, and do not submit sensitive or regulated images unless that external processing is authorized.

Risk: The script uses a hard-coded user site-packages path for Python dependencies.

Mitigation: Run the skill in an isolated virtual environment with trusted, pinned dependencies and remove or avoid the hard-coded dependency path before deployment.

Risk: The security verdict is suspicious despite no specific risk findings.

Mitigation: Review the skill before installing and scan it as part of deployment approval.

## Reference(s):

- [Jimeng Video Prompt Guide](references/prompt-guide.md)
- [Volcano Engine Visual API Endpoint](https://visual.volcengineapi.com)
- [ClawHub Skill Page](https://clawhub.ai/sdt328606/skills/stitch-jimeng-video)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, API Calls, Files, Guidance]

**Output Format:** [Markdown guidance with command-line examples and generated MP4 video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VOLC_ACCESS_KEY and VOLC_SECRET_KEY credentials; can submit a job without polling when requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
