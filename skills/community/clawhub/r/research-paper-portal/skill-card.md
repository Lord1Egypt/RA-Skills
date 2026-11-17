## Description:

Research Paper Portal helps researchers build a personalized academic paper navigation site that collects recent papers, generates AI background images, and publishes scheduled updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiaxiliao](https://clawhub.ai/user/jiaxiliao)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, research groups, and developers use this skill to configure and publish a paper portal for a chosen research area. The skill guides paper collection from academic sources, LLM-assisted title and summary generation, ComfyUI-based background image creation, and scheduled publication of the resulting site data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scheduled paper-ingestion workflow can pass untrusted paper metadata into a shell-based LLM invocation.

Mitigation: Do not schedule the ingestion script until the LLM call avoids shell execution or strictly sanitizes and validates all metadata used in command construction.

Risk: Generated paper data can include external paper URLs that are rendered into the portal.

Mitigation: Validate paper URLs against allowed schemes and render paper fields as text before publishing data from external paper sources.

Risk: The image-generation script sends prompts and downloads outputs from a configured ComfyUI endpoint.

Mitigation: Use a trusted local or protected ComfyUI endpoint and run the scripts under a dedicated low-privilege account.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiaxiliao/skills/research-paper-portal)
- [Publisher Profile](https://clawhub.ai/user/jiaxiliao)
- [API Usage Reference](references/API.md)
- [ComfyUI Flux2 Workflow Reference](references/COMFYUI.md)
- [Configuration Reference](references/CONFIG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, Python scripts, and HTML/CSS/JavaScript template files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces portal configuration guidance, scheduled publishing commands, paper queue JSON, paper index JSON, WebP image assets, and a static website template.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
