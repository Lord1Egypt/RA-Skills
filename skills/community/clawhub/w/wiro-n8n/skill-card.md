## Description:

Generate video, images, speech, music, 3D and LLM output with Wiro AI inside n8n workflows through the Wiro AI community node @wiro-ai/n8n-nodes-wiro, including install, the Wiro AI API credential, picking a model and its inputs, task outputs, errors and cost control. Use when the user builds an n8n workflow or automation with Wiro, asks about the Wiro AI node or @wiro-ai/n8n-nodes-wiro, or wants media or LLM output generated in n8n.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiroai](https://clawhub.ai/user/wiroai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and n8n workflow builders use this skill to install and configure the Wiro AI community node, choose a model and its inputs, and build workflows that generate media or text through Wiro AI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and referenced files sent through the workflow may contain sensitive information and are sent to Wiro for processing.

Mitigation: Use only information approved for processing by Wiro; review prompt content and file URLs before enabling a workflow.

Risk: The installation command is unpinned, and the security analysis had incomplete coverage because two referenced local paths could not be resolved.

Mitigation: Review the install command and fetched skill content before installing or enabling the node, and verify the package version with an administrator.

## Reference(s):

- [n8n community node installation](https://docs.n8n.io/integrations/community-nodes/installation/)
- [Wiro authentication](https://wiro.ai/docs/authentication)
- [Wiro model catalog](https://wiro.ai/models)
- [Wiro model parameters](https://wiro.ai/docs/model-parameters)
- [Wiro pricing](https://wiro.ai/product/pricing)
- [Wiro n8n integration guide](https://wiro.ai/docs/n8n-wiro-integration)
- [Wiro n8n community node package](https://www.npmjs.com/package/@wiro-ai/n8n-nodes-wiro)
- [Project link listed in the skill](https://github.com/wiroai/n8n-nodes-wiro)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, model input, task output, error handling, and cost guidance.]

## Skill Version(s):

2.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
