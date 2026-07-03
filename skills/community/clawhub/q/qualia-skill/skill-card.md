## Description: <br>
Fine-tune robotic foundation models on Qualia cloud GPUs from an agent CLI, including launching, monitoring, and canceling training jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fabbe1999](https://clawhub.ai/user/fabbe1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to fine-tune Vision-Language-Action and related robot models with LeRobot-format HuggingFace datasets, then monitor or manage the resulting Qualia training jobs from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can launch paid Qualia training jobs and change account resources such as projects and running jobs. <br>
Mitigation: Require explicit user confirmation before paid training launches, project deletion, or job cancellation, and check credits and estimated cost before launching. <br>
Risk: The skill requires a Qualia API key that can access credits and manage training workflows. <br>
Mitigation: Use a limited or revocable API key where available, keep the key out of prompts and logs, and install only when the publisher is trusted. <br>


## Reference(s): <br>
- [Qualia](https://qualiastudios.dev) <br>
- [Qualia App](https://app.qualiastudios.dev) <br>
- [Qualia LLM Context](https://docs.qualiastudios.dev/llms.txt) <br>
- [Qualia API Reference](https://dev-docs.qualiastudios.dev/api/reference) <br>
- [Qualia SDK](https://docs.qualiastudios.dev/sdk/overview/) <br>
- [Qualia Guides](https://docs.qualiastudios.dev/global/guides/) <br>
- [ClawHub Skill Page](https://clawhub.ai/fabbe1999/skills/qualia-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands support a --json mode that emits one JSON object or array on stdout with stable exit codes.] <br>

## Skill Version(s): <br>
2.1.1 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
