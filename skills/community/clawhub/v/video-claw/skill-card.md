## Description:

End-to-end video creation copilot for OpenClaw that helps users brainstorm ideas, research angles, generate hooks and teleprompter scripts, create recording links, process interviews, edit transcripts and video cuts, render final outputs, and publish content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chin-jlyc](https://clawhub.ai/user/chin-jlyc)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and OpenClaw users use this skill to plan social video topics, create hooks and teleprompter scripts, open recording links, refine uploaded clips, and prepare final publishing copy. It is especially oriented toward personal-branding video workflows that move from idea to preview-first editing and optional publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to paste a long-lived Humeo personal access token into chat and stores it locally for reuse.

Mitigation: Review token handling before installation, use the least-scoped token available, keep the token file permission-restricted, and revoke or rotate the token when it is no longer needed.

Risk: The skill creates persistent reminder jobs that continue using the stored token in the background.

Mitigation: Make reminder setup opt-in, inspect scheduled VideoClaw jobs after setup, and remove jobs that are no longer needed.

Risk: Publishing workflows can send rendered videos to external social platforms when upload credentials are configured.

Mitigation: Require explicit user approval before final download or publishing, keep publishing credentials outside the skill, and review platform results after upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chin-jlyc/skills/video-claw)
- [Publisher profile](https://clawhub.ai/user/chin-jlyc)
- [Humeo app](https://app.humeo.com)
- [Humeo Personal Access Token setup](https://app.humeo.com/profile/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown text with recording links, preview links, scripts, captions, checklist-style guidance, and occasional setup or debugging commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce creator-facing hooks, scripts, edit instructions, render guidance, reminder setup steps, and publishing preparation; defaults to preview-first delivery before final download or publishing.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
