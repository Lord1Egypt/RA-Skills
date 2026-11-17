## Description:

Generate qPCR/ELISA dilution protocols with precise pipetting steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and laboratory developers use this skill to generate serial dilution concentration tables and pipetting instructions for qPCR standard curves, ELISA plate setup, drug dose responses, and MIC determinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated wet-lab dilution guidance may be scientifically incomplete because the security evidence notes that the implementation ignores the documented target/final concentration.

Mitigation: Manually verify the dilution series, target concentration, and pipetting volumes before using the output for laboratory work.

Risk: Future versions that add file outputs could create workspace file-handling risk if paths are not clearly documented or constrained.

Mitigation: Review any documented file outputs and keep generated files restricted to the intended workspace before deployment.

## Reference(s):

- [Serial Dilution Calculator on ClawHub](https://clawhub.ai/aipoch-ai/skills/serial-dilution-calculator)
- [aipoch-ai Publisher Profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text CLI output with concentration and pipetting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally without additional Python package dependencies.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
