## Description: <br>
End-to-end video creation copilot for OpenClaw that helps users brainstorm ideas, research angles, generate hooks and teleprompter scripts, create recording links, process interviews, edit transcripts and video cuts, render final outputs, and publish content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chin-jlyc](https://clawhub.ai/user/chin-jlyc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and operators use this skill to plan social media videos, create scripts and recording links, process recorded interviews, refine clips, render final outputs, and prepare publishing copy. It is most useful for personal-branding and recurring content workflows in OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for a reusable Humeo Personal Access Token and stores it locally for future use. <br>
Mitigation: Review before installing, use a revocable least-privilege token when available, keep the token file permission-restricted, and rotate or delete the token when the skill is no longer needed. <br>
Risk: Background reminder jobs can act and send messages after setup. <br>
Mitigation: Inspect OpenClaw cron entries after setup, verify the selected notification channel, and remove unwanted reminder jobs. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/chin-jlyc/video-claw) <br>
- [Humeo application](https://app.humeo.com) <br>
- [Humeo Personal Access Token setup](https://app.humeo.com/profile/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text, configuration] <br>
**Output Format:** [Markdown and plain text responses with creator-facing links and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create recording links, calendar reminders, preview links, render requests, and publishing copy when configured by the user.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
