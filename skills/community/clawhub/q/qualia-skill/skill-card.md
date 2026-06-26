## Description: <br>
Fine-tune robot foundation models on Qualia cloud GPUs, including VLA, pi0, pi0.5, GR00T N1.5, ACT, SmolVLA, and SARM workflows, while launching, monitoring, and cancelling training jobs from an agent-friendly CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fabbe1999](https://clawhub.ai/user/fabbe1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to let an agent manage Qualia robot-model fine-tuning workflows, including model selection, dataset key inspection, project creation, training launches, status monitoring, cancellation, and hyperparameter validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend Qualia credits by launching cloud training jobs. <br>
Mitigation: Require explicit user confirmation before starting paid training and estimate cost from available instances before launch. <br>
Risk: The skill requires a sensitive QUALIA_API_KEY credential. <br>
Mitigation: Keep the key private, use an account or key with appropriate limits, and avoid logging or sharing the key. <br>
Risk: The skill can delete Qualia projects. <br>
Mitigation: Require explicit confirmation and verify the target project ID before running project-delete. <br>


## Reference(s): <br>
- [Qualia](https://qualiastudios.dev) <br>
- [Qualia App](https://app.qualiastudios.dev) <br>
- [Qualia LLM Context](https://docs.qualiastudios.dev/llms.txt) <br>
- [Qualia API Reference](https://dev-docs.qualiastudios.dev/api/reference) <br>
- [Qualia SDK Overview](https://docs.qualiastudios.dev/sdk/overview/) <br>
- [Qualia Guides](https://docs.qualiastudios.dev/global/guides/) <br>
- [ClawHub Skill Page](https://clawhub.ai/fabbe1999/qualia-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional machine-readable JSON from the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI supports a global --json flag for one JSON object or array on stdout and stable exit codes for agent control flow.] <br>

## Skill Version(s): <br>
2.1.0 (source: SKILL.md frontmatter, CHANGELOG, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
