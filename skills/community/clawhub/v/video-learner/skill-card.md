## Description:

Analyze video content and generate a callable Skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keke-skills](https://clawhub.ai/user/keke-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn user-provided Douyin, BiliBili, or YouTube videos into analyzed transcripts and, after explicit confirmation, a generated SKILL.md for a new callable skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent skills from video-derived content, and server security evidence says its safeguards for untrusted transcripts and user review are thin for that authority.

Mitigation: Review the generated SKILL.md before installation, stage generated skills outside active skill directories until independently checked, and scan generated content before deployment.

## Reference(s):

- [Video Learner ClawHub skill page](https://clawhub.ai/keke-skills/skills/video-learner)
- [keke-skills publisher profile](https://clawhub.ai/user/keke-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown and generated SKILL.md files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download temporary video files, transcribe audio locally with Whisper, and write generated skills under ~/.openclaw/workspace/skills/ after user confirmation.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
