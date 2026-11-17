## Description:

This skill guides agents in using Ruhui, a self-hosted bilingual System 1 decision engine, for bounded semantic judgments with typed choice, noul, and score outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyforge](https://clawhub.ai/user/anyforge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to replace brittle prompt-and-parse steps with local, typed semantic decisions for routing, ranking, extraction, verification, moderation, and triage. It is especially relevant when applications need offline operation, bilingual Chinese and English inputs, or calibrated probabilities for bounded choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production use depends on trusting the Python package and downloaded model checkpoints.

Mitigation: Verify the intended PyPI package and model repositories before installation, and pin package versions or model hashes for production deployments.

Risk: Typed probabilities can still be incorrect or poorly calibrated for a target domain.

Mitigation: Validate on representative cases, choose thresholds from domain data, and escalate low-confidence or high-impact decisions to human review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anyforge/skills/ruhui)
- [Hugging Face model repository](https://huggingface.co/anyforge/ruhui)
- [ModelScope model repository](https://www.modelscope.cn/models/anyforge/ruhui)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on local model download, backend selection, typed decision primitives, and validation practices.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
