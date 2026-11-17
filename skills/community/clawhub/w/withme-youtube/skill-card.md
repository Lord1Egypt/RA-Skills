## Description:

Withme Youtube coordinates a Lofi ambient YouTube video workflow from topic selection through AI image generation, Envato audio preparation, FFmpeg assembly, SEO assets, upload scheduling, and Shorts cutdowns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylin19860916](https://clawhub.ai/user/kylin19860916)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and channel operators use this skill to plan, assemble, package, and schedule long-form Lofi ambience videos for YouTube. It guides agent handoffs for visual generation, audio selection, FFmpeg composition, metadata preparation, and publishing checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow relies on credentials and a logged-in browser session for media download and YouTube publishing.

Mitigation: Use restricted Google and YouTube credentials, isolate the Envato browser profile, and install only for trusted personal workflows.

Risk: Automated download and publishing steps can proceed with limited containment or final user control.

Mitigation: Stage downloads separately and require final explicit approval that shows the resolved channel, file hashes, title, thumbnail, visibility, and schedule before upload.

Risk: Shared scripts, credentials, browser profile, and upload queue may be modified outside the skill.

Mitigation: Verify those files and settings before each release run, and review the generated upload queue before executing the uploader.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kylin19860916/skills/withme-youtube)
- [Content Matrix](references/content-matrix.md)
- [Visual Style Guide and Prompt Template](references/style-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, Python, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow instructions, file path conventions, FFmpeg template parameters, upload queue structure, and review checkpoints.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
