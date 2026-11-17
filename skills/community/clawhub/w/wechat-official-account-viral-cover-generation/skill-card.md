## Description:

Helps agents create and edit WeChat Official Account main covers, sharing cards, and series visuals with Nano Banana Pro while keeping the article promise, core argument, and crop-safe areas aligned.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, editors, and marketers use this skill to generate WeChat Official Account cover images, sharing cards, and recurring column visuals from article summaries or authorized reference images. The skill supports prompt planning, crop-preview discipline, API key setup, image generation, task polling, and result download through AI Hive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts and optional reference images to the AI Hive image service.

Mitigation: Upload only images the user is authorized to share and avoid including unnecessary sensitive content in prompts or files.

Risk: API keys can be exposed if passed directly on the command line or stored with loose permissions.

Mitigation: Prefer the documented environment variable or config file flow, avoid command-line secrets, and keep local key files restricted.

Risk: Downloaded image results may be untrusted files.

Mitigation: Treat generated downloads as untrusted until opened, scanned, or processed with normal local file-safety practices.

Risk: WeChat cover dimensions, sharing crops, or platform behavior may change after generation.

Mitigation: Review the main cover, sharing card, and history-feed crop in the current WeChat backend before publication.

Risk: The term viral could imply performance certainty that the skill does not provide.

Mitigation: Use the generated cover as a publication asset, not as a guarantee of readership or conversion results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/wechat-official-account-viral-cover-generation)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash command examples and downloaded image files, typically PNG outputs from completed generation tasks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an AI Hive API key, fixed Nano Banana Pro image model, optional authorized image inputs, batch size, routing preference, image parameters such as aspect ratio, and task IDs for polling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
