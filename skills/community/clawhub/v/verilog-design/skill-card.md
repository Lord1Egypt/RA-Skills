## Description:

Designs, implements, and verifies Verilog/SystemVerilog modules using spec-driven development, self-checking testbenches, static slang checks, simulator workflows, and VCD waveform analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billchen1020](https://clawhub.ai/user/billchen1020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and hardware engineers use this skill to create Verilog/SystemVerilog modules, write design specs and testbenches, run available local simulators, and analyze VCD waveforms during verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local simulator commands can execute installed EDA tools and create design, testbench, log, and waveform files in the workspace.

Mitigation: Run verification in an isolated project workspace and review generated files and simulator commands before execution.

Risk: The VCD analysis helper depends on the third-party Python package vcdvcd.

Mitigation: Install dependencies in a virtual environment and pin or review vcdvcd before using the skill in CI or sensitive workspaces.

Risk: The waveform analysis scripts are built for VCD and do not support FSDB waveform files.

Mitigation: Configure testbenches to emit VCD with $dumpfile and $dumpvars before using the analysis workflow.

## Reference(s):

- [VCD Waveform Analysis with Python](references/vcd-analysis.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Verilog/SystemVerilog code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create design specs, Verilog/SystemVerilog source files, self-checking testbenches, simulation logs, VVP files, and VCD waveforms in the user's workspace.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
