## Description:

Avoid common PyTorch mistakes -- train/eval mode, gradient leaks, device mismatches, and checkpoint gotchas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill as quick reference guidance for avoiding common PyTorch training, inference, device, DataLoader, checkpoint, autograd, and memory-management mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checkpoint-loading guidance may be copied without enough safety checks for untrusted model files.

Mitigation: Load checkpoints only from trusted sources, prefer torch.load(..., weights_only=True) where supported, and verify model files before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/pytorch)

## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Markdown guidance with inline PyTorch code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise reference material; no active code execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
