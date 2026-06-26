## Description: <br>
可以生成数字人口播视频。训练自己的数字人、生成口播视频。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuhongfeii2](https://clawhub.ai/user/xuhongfeii2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to list available digital humans and voices, train custom digital humans or voices, and submit talking-head video synthesis tasks through the configured platform API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses HTTP defaults for the platform API and may transmit media, scripts, callback details, and credentials over that connection. <br>
Mitigation: Install only when the EasyClaw/Chanjing platform is trusted, prefer short-lived API tokens, and rotate tokens after use. <br>
Risk: Scheduled watcher commands may persist credential-related environment details on the machine where the agent runs. <br>
Mitigation: Avoid shared machines for sensitive work and review or remove scheduled watchers after task completion. <br>


## Reference(s): <br>
- [Platform API Reference](references/platform-api.md) <br>
- [Setup Guide](references/setup.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xuhongfeii2/shuziren-koubo-shengcheng) <br>
- [Publisher Profile](https://clawhub.ai/user/xuhongfeii2) <br>
- [Chanjing API Keys](https://www.chanjing.cc/platform/api_keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline media links and JSON-backed task results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include direct image and video URLs returned by platform tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
