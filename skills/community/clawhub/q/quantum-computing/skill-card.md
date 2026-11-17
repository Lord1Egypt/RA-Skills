## Description:

Helps agents answer UnifiedQuantum and uniqc questions covering circuit building, OriginIR and OpenQASM export, local simulation, cloud submission, variational algorithms, quantum ML, and PyTorch integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agony5757](https://clawhub.ai/user/agony5757)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get concise guidance, code examples, shell commands, and troubleshooting steps for UnifiedQuantum workflows. It is especially suited to building and converting circuits, running local or dummy simulations, configuring cloud backends, and adapting VQE, QAOA, UCCSD, and PyTorch examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud backend tokens and real hardware submissions can expose sensitive credentials or consume quota and budget.

Mitigation: Enter tokens only in the intended environment, confirm the selected backend before submission, and use dummy or local simulation modes for testing when possible.

Risk: Installing UnifiedQuantum extras into a shared Python environment can change dependency state for unrelated projects.

Mitigation: Prefer an isolated virtual environment or tool installation, and install only the extras required for the requested workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agony5757/skills/quantum-computing)
- [UnifiedQuantum repository](https://github.com/IAI-USTC-Quantum/UnifiedQuantum)
- [UnifiedQuantum release notes](https://iai-ustc-quantum.github.io/UnifiedQuantum/source/releases/index.html)
- [Circuit building reference](references/circuit-building.md)
- [CLI usage reference](references/cli-guide.md)
- [Simulator reference](references/simulators.md)
- [Cloud platform reference](references/cloud-platforms.md)
- [Variational algorithms reference](references/variational-algorithms.md)
- [PyTorch integration reference](references/pytorch-integration.md)
- [H2 molecular simulation reference](references/h2-molecular-simulation.md)
- [Troubleshooting reference](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline code and command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Python examples, uniqc CLI commands, installation options, backend configuration guidance, and troubleshooting checklists.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
