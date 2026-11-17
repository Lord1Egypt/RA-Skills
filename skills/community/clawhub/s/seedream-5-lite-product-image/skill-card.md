## Description:

Helps agents generate Seedream 5.0 Lite product photography, hero images, scene images, detail views, package contents, and SKU image sets through AI Hive while preserving product structure and brand facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users, merchants, and creative teams use this skill to guide an agent through Seedream 5.0 Lite product-image generation for ecommerce main images, product scenes, detail views, package contents, and consistent SKU variants. The workflow emphasizes an approved product photography master before batch variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected product or reference images and prompts are sent to AI Hive for generation.

Mitigation: Use only images and prompts that are approved for AI Hive processing, and avoid confidential, embargoed, or personally sensitive product material unless policy allows it.

Risk: The skill stores an AI Hive API key locally for CLI use.

Mitigation: Prefer environment variables or the initialized config file with restricted permissions, rotate keys if exposed, and avoid committing local configuration.

Risk: The install example uses an unpinned requests dependency.

Mitigation: Install in a virtual environment and pin dependency versions according to the consuming organization's package policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedream-5-lite-product-image)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash command examples; the CLI can emit JSON task data and download generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI Hive API credentials, accepts optional reference images, supports batch image generation, and can save outputs to a local directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact changelog top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
