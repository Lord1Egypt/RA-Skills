## Description: <br>
Provides Tinker SDK, CLI, checkpoint, Hugging Face export, and tinker-cookbook training workflow guidance for agents assisting with model fine-tuning and training operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zjrwtx](https://clawhub.ai/user/zjrwtx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML engineers use this skill to operate Tinker training runs, inspect and manage checkpoints, export adapters, configure cookbook recipes, and troubleshoot Tinker SDK or CLI issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checkpoint deletion and TTL commands can permanently remove or expire training assets. <br>
Mitigation: Verify the exact Tinker path, run ID, filters, workspace ownership, and backup requirements before running delete or TTL commands. <br>
Risk: Publishing checkpoints or pushing adapters to Hugging Face can expose proprietary weights, training data traces, or sensitive metadata. <br>
Mitigation: Confirm repository visibility, license, organization ownership, file include/exclude patterns, and model card contents before any publish, public, or push-hf operation. <br>
Risk: Authentication and experiment logging workflows require API keys or third-party tokens. <br>
Mitigation: Use scoped credentials, avoid pasting secrets into shared transcripts, and confirm W&B or Hugging Face account targets before logging in or uploading outputs. <br>


## Reference(s): <br>
- [Tinker CLI - Full Command Reference](references/cli-reference.md) <br>
- [Tinker Cookbook - Recipe Deep-Dives](references/cookbook-recipes.md) <br>
- [Tinker Troubleshooting Guide](references/troubleshooting.md) <br>
- [Tinker SDK Repository](https://github.com/thinking-machines-lab/tinker) <br>
- [Tinker Cookbook Repository](https://github.com/thinking-machines-lab/tinker-cookbook) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that modify checkpoint visibility, retention, deletion, external publishing, or experiment logging; users should review targets and credentials before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
