## Description: <br>
可调用 banana、sora、veo 等模型生成图片视频，适合图片、视频与短剧素材生产。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuhongfeii2](https://clawhub.ai/user/xuhongfeii2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to submit image and video generation jobs through the EasyClaw platform relay for Banana, Sora, and VEO models. It supports guided script-based submission, task lookup, and optional watcher delivery for completed results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, uploaded media, API tokens, and task results through the EasyClaw relay, and the security summary notes plaintext HTTP transport by default. <br>
Mitigation: Install only when the relay is trusted, prefer an HTTPS base URL where available, and avoid sending sensitive prompts or reference media. <br>
Risk: Default watcher behavior can read session data and post final results back into chats or transcripts. <br>
Mitigation: Use --no-watch when background delivery is not needed, inspect created cron jobs, and verify the notification target before submitting a generation job. <br>
Risk: Credentials may be exposed through plaintext transport, query strings, or command-line arguments. <br>
Mitigation: Use environment variables for tokens where possible and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xuhongfeii2/tupian-shipin-shengcheng) <br>
- [Setup](references/setup.md) <br>
- [Platform Relay API](references/platform-api.md) <br>
- [Model Guide](references/model-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generation requests may create background watcher jobs unless --no-watch is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
