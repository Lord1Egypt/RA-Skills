## Description:

Helps creators, brand visual teams, music-content teams, and advertisers design and generate seamless looping short videos with start/end frame planning, prompts, AI-HIVE task commands, and quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, brand visual teams, marketers, and agent developers use this skill to turn a looping short-video brief into a storyboard, prompts, AI-HIVE generation commands, task records, downloadable video outputs, and acceptance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A stored API key can be sent to an unexpected AI-HIVE base URL if AI_HIVE_BASE_URL or the local config base_url is changed.

Mitigation: Use the default AI-HIVE endpoint, remove unexpected base URL overrides, and review credential handling before installing or running generation commands.

Risk: Reference media and prompts may be uploaded to the AI-HIVE service during generation.

Mitigation: Upload only media the user is authorized to use and avoid sensitive media unless the service is trusted for that data.

Risk: Authenticated image or video generation calls may incur charges.

Mitigation: Review prompts, model mode, routing choice, and pricing snapshot before submitting tasks; test batch work with a small sample first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seamless-loop-video-ai-hive)
- [AI-HIVE web app](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, JSON task records, and generated or edited media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON blueprints and video files; authenticated AI-HIVE generation may incur charges.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
