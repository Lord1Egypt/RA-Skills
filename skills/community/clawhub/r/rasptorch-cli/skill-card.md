## Description:

Operate rasptorch (NumPy deep learning library) via its agent-native CLI, consuming JSON output. Supports tensors, model creation (mlp, cnn, cv, jev, gru, transformer, linear), training, save/load, and UI/chat modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joshua-ludolf](https://clawhub.ai/user/joshua-ludolf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create and manage tensors and neural network models, inspect runtime capabilities, and run model workflows through rasptorch's CLI while consuming structured JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rated the skill benign with medium confidence because one scan was partial and could not resolve three references.

Mitigation: Review the referenced material and the commands before installation, especially before running training or file-writing operations.

Risk: Model training can use significant compute, and save/load commands write files.

Mitigation: Use small workloads by default and review the target path before saving or loading model files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joshua-ludolf/skills/rasptorch-cli)
- [Publisher profile](https://clawhub.ai/user/joshua-ludolf)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Structured JSON from rasptorch CLI commands, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI model operations are stateful within a session; UI and chat modes can run long-lived processes.]

## Skill Version(s):

2.1.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
