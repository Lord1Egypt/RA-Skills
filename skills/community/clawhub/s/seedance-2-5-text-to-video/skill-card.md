## Description:

Seedance 2.5 文生视频 helps creators, marketing teams, e-commerce teams, and short-form video producers generate videos from Chinese or English text prompts through AI Hive, with task tracking and result download support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Seedance 2.5 text-to-video jobs, manage task IDs, and download generated video assets for advertising, e-commerce, product demos, social media, short drama, and comic-style video production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A malicious or compromised custom AI Hive endpoint could expose an API key.

Mitigation: Use the default AI Hive endpoint unless the custom endpoint is fully trusted, and avoid passing API keys on the command line.

Risk: Downloaded result files could overwrite local files or be placed in an unsafe location.

Mitigation: Run the skill from an isolated environment and choose an output directory where accidental overwrites are low impact.

Risk: Saved credentials could be exposed if the local configuration file is mishandled.

Mitigation: Keep the saved config file private and review the skill before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-2-5-text-to-video)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Files]

**Output Format:** [Markdown guidance with shell commands; runtime commands can return JSON task data and downloaded video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is downloaded to a user-selected output directory, defaulting to ~/Downloads/AiHive.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
