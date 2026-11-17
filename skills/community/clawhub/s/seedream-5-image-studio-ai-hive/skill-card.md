## Description:

Seedream 5 图片工作室｜AI-HIVE helps image creators, brand designers, and ecommerce visual teams turn Seedream 5 image requests into prompts, reference-image plans, batch variants, AI-HIVE generation commands, and delivery checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External image creators, brand designers, and ecommerce visual teams use this skill to plan and run Seedream 5 image-generation or image-editing work for ecommerce, advertising, marketing, social media, short drama, and commerce content. It supports fact gathering, authorized reference-material planning, prompt creation, AI-HIVE routing, small-batch generation, task tracking, result downloads, and delivery review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API keys for AI-HIVE generation and may store credentials in local configuration.

Mitigation: Install only if the AI-HIVE publisher is trusted, keep API keys scoped and revocable, avoid writing keys into prompts or repositories, and remove or rotate keys when access is no longer needed.

Risk: Custom base URLs or server-provided media URLs could direct uploads or downloads to destinations the user did not intend.

Mitigation: Use the default AI-HIVE endpoint unless the endpoint is controlled and trusted, and review generated commands before running uploads, downloads, or task polling.

Risk: Generation tasks may incur charges and can use uploaded reference media.

Mitigation: Confirm prompts, routing mode, model choice, batch size, price snapshot, and media authorization before submitting generation jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedream-5-image-studio-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, Python command examples, JSON task records, and generated file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON briefs, upload authorized media, submit potentially billed AI-HIVE generation tasks, poll asynchronous task status, and download generated media files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
