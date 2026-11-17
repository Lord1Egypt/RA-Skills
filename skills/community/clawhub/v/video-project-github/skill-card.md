## Description:

Sets up a private GitHub backup for video or agent-built projects, with saved versions, media tracking, and restore guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to organize a video or agent-built project, back it up to a private GitHub repository, track media, and restore it on another computer without needing to learn Git.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project files or credentials could be exposed through upload, file handling, or access settings.

Mitigation: Check repository visibility and invite access before uploading; keep credentials and sensitive files out.

Risk: Rollback or restore may not return the intended project state safely.

Mitigation: Try proof and restore on a disposable copy, then compare file hashes before relying on the backup.

Risk: Media may be mishandled or exposed when stored separately from project files.

Mitigation: Review which media is uploaded and where it is stored; exclude sensitive media unless its access controls are confirmed.

## Reference(s):

- [Project homepage listed in skill metadata](https://github.com/vargHQ/skills/tree/main/video-project-github)
- [Keep a video project in GitHub guide](https://varg.ai/how-to/keep-a-video-project-in-github)
- [How to make a video with an AI agent](https://varg.ai/how-to/make-a-video-in-ten-steps)

## Skill Output:

**Output Type(s):** [Project files, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown instructions, shell commands, and project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates a project folder and its versioned backup; media storage and access depend on repository settings.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
