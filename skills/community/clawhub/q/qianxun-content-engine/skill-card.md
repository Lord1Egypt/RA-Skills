## Description:

内容引擎 helps an agent deconstruct Xiaohongshu posts into structured analysis cards and generate brand-adapted scripts, captions, cover copy, tags, image prompts, reference images, and video outputs from those analyses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dizhu](https://clawhub.ai/user/dizhu)

### License/Terms of Use:

MIT-0

## Use Case:

Content strategists, marketers, and developers use this skill to study high-performing Xiaohongshu posts and create brand-adapted social content packages. Agents can use it for structured content deconstruction, reusable knowledge-graph updates, script generation, copy generation, reference-image generation, and configured short-video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses paid API credentials for content extraction, LLM/image generation, and optional video generation.

Mitigation: Use dedicated low-limit API keys, store them with restricted permissions, run small counts first, and review cost-sensitive video generation before enabling unattended runs.

Risk: Fallback or custom provider endpoints can send prompts, links, or generated content to an unintended service.

Mitigation: Avoid OPENROUTER_API_KEY fallback unless the endpoint is explicitly correct, and only set custom BASE_URL values for trusted HTTPS provider hosts.

Risk: Persistent graph write-backs can add inaccurate brand, platform, style, or hook knowledge that affects future generations.

Mitigation: Require manual review of graph write-backs before relying on them in future content workflows.

Risk: Skipping confirmation for video generation can trigger paid or unwanted generation work.

Mitigation: Keep confirmation enabled for normal use, reserve --no-confirm for controlled automation, and inspect partial-video reports when any shot fails.

## Reference(s):

- [Output template](artifact/references/output-template.md)
- [Video deconstruction example](artifact/references/example-video.md)
- [Image deconstruction example](artifact/references/example-image.md)
- [Xiaohongshu platform playbook](artifact/graph/platforms/xiaohongshu.md)
- [TikHub](https://tikhub.io)
- [Ofox](https://ofox.ai)
- [Volcengine Ark API key console](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey)
- [OpenRouter](https://openrouter.ai)
- [Ronin content-engine architecture reference](https://x.com/DeRonin_/status/2042604279077237170)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, plain text files, shell commands, Python script outputs, image/video generation prompts, generated media file paths, and optional MP4 video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local workspaces, deconstruction cards, generated-content directories, graph append-only updates, reference images, per-shot videos, partial-video reports, and a concatenated final video when the required services are configured.]

## Skill Version(s):

0.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
