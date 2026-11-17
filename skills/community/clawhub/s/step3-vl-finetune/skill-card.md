## Description:

Guides agents through configuring, training, troubleshooting, and using LoRA or full fine-tuning workflows for the Step3-VL-10B multimodal model on Linux GPU servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hunwenpinghao](https://clawhub.ai/user/hunwenpinghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML engineers use this skill to prepare Step3-VL-10B fine-tuning runs, configure GPU training environments, save LoRA adapters, and run inference with the fine-tuned model. The guidance is most useful for Linux GPU server workflows that need practical troubleshooting steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide contains environment-specific server, registry, internal IP, endpoint, and document path details.

Mitigation: Replace these details with deployment-specific placeholders before installation or sharing, and avoid sending data to the listed endpoint unless the network and access controls are approved.

Risk: The documented workaround may train only the language component while presenting the workflow as multimodal fine-tuning.

Mitigation: Validate whether the vision encoder is active before claiming full multimodal fine-tuning, and document language-only behavior when using the monkey-patched forward path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hunwenpinghao/skills/step3-vl-finetune)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash, Python, JSON, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets Linux GPU environments requiring python3 and CUDA_VISIBLE_DEVICES; environment-specific endpoints, paths, and registry names should be replaced before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
