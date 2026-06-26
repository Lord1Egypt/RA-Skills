## Description: <br>
Video Monetization Pro automates a creator workflow for trend analysis, MV topic selection, lyric drafting, compliance review, Suno prompting, storyboarding, multi-platform publishing, and revenue monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dahuangfortoby](https://clawhub.ai/user/dahuangfortoby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators and creator teams use this skill to plan monetized music-video content, generate production assets, prepare platform publishing steps, and monitor revenue reports across supported channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports exposed real-looking service credentials. <br>
Mitigation: Remove the exposed values, rotate any affected credentials, and replace them with user-owned scoped secrets before installation or use. <br>
Risk: The security review reports broad account-impacting publishing, OAuth or logged-session use, revenue monitoring, Feishu delivery, and persistent report storage behavior. <br>
Mitigation: Require explicit per-platform confirmation before publishing, account access, report delivery, or persistent storage actions. <br>
Risk: Generated legal, monetization, and platform-compliance guidance may be incomplete or inaccurate. <br>
Mitigation: Review generated content and compliance results before publishing or relying on revenue-related recommendations. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/dahuangfortoby/video-monetization-pro-84) <br>
- [OpenClaw homepage declared by the skill](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and shell-command guidance with generated planning, compliance, publishing, and revenue-report text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg and whisper binaries plus user-provided Suno and Kling credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
