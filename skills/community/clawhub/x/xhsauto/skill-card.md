## Description:

Automates a Xiaohongshu content workflow by turning a topic into draft copy, generated or supplied images, and a debug publish validation report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luweizheng](https://clawhub.ai/user/luweizheng)

### License/Terms of Use:


## Use Case:

Content creators, marketers, and agent developers use this skill to draft Xiaohongshu notes, produce supporting images through configured image APIs, and validate content with xhs-kit before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can interact with Xiaohongshu publishing workflows through xhs-kit.

Mitigation: Run debug-publish first, verify login state deliberately, and review all generated content before using any formal publish command.

Risk: Prompts, selected images, and generated content may be sent to configured Google/Gemini or ByteDance Seed API gateways.

Mitigation: Avoid sensitive draft content or private images, prefer official HTTPS endpoints, and use restricted API keys.

Risk: Dependency and gateway behavior depends on local installations and environment variables.

Mitigation: Use a virtual environment, pin and review dependency versions, and confirm GOOGLE_API_KEY, GEMINI_API_KEY, or SEED_API_KEY scopes before execution.

## Reference(s):

- [xhs-auto on ClawHub](https://clawhub.ai/luweizheng/skills/xhsauto)
- [Text-to-image and image editing guide](references/text-to-image.md)
- [Xiaohongshu publishing and validation guide](references/publish.md)
- [Google OpenAI-compatible image API base](https://generativelanguage.googleapis.com/openai)
- [ByteDance Seed API base](https://seed.bytedanceapi.com)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, JSON]

**Output Format:** [Markdown drafts, generated image files, shell commands, and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes draft content and image paths under workspace/xhs-auto/{timestamp}; image scripts emit JSON status for agent parsing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
