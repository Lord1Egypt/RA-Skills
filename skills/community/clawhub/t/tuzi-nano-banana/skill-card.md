## Description:

Generate/edit images via Tuzi API (default), Google Gemini, OpenAI, DashScope, Replicate. Text-to-image + image-to-image editing; 1K/2K/4K resolution. Use for image create/modify/edit requests incl. --input-image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljquan](https://clawhub.ai/user/ljquan)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to generate new PNG images or edit existing images through supported image-generation providers. It is suited for normal ClawHub image creation and modification workflows where API keys are supplied by the user environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell execution paths could let crafted inputs run local commands or expose API credentials.

Mitigation: Review and patch the unsafe shell paths before use with untrusted filenames, environment variables, or API-key inputs; run the skill in a restricted environment.

Risk: Prompts, input images, and generated outputs are sent to external image-generation providers selected by configuration and available API keys.

Mitigation: Avoid sensitive prompts or images, use narrowly scoped API keys, and only enable trusted providers, proxies, and custom base URLs.

Risk: Runtime installation through npx and bun can introduce supply-chain or version drift risk.

Mitigation: Prefer a pinned or preinstalled Bun runtime and review dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ljquan/skills/tuzi-nano-banana)
- [ClawHub publisher profile](https://clawhub.ai/user/ljquan)
- [Tuzi API](https://api.tu-zi.com)
- [Tuzi API token page](https://api.tu-zi.com/token)
- [Google Generative Language API](https://generativelanguage.googleapis.com)
- [OpenAI API](https://api.openai.com/v1)
- [DashScope API](https://dashscope.aliyuncs.com)
- [Replicate API](https://api.replicate.com)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PNG image files with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves generated or edited PNG files to the current working directory or specified output path.]

## Skill Version(s):

1.0.0 (source: artifact/_meta.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
