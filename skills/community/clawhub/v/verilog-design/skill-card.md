## Description: <br>
Design, implement, and verify Verilog/SystemVerilog modules with spec-driven development, self-checking testbenches, and automated simulation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billchen1020](https://clawhub.ai/user/billchen1020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and hardware engineers use this skill to turn digital design requirements into Verilog/SystemVerilog modules, self-checking testbenches, simulation commands, and waveform-analysis guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HDL or testbenches may contain incorrect logic or local command execution through Verilog system tasks. <br>
Mitigation: Review generated modules and testbenches before simulation, with particular attention to any $system calls. <br>
Risk: Simulation and waveform analysis rely on local EDA tools and Python dependencies. <br>
Mitigation: Install and run simulator and Python dependencies in a controlled environment. <br>


## Reference(s): <br>
- [VCD Waveform Analysis with Python](references/vcd-analysis.md) <br>
- [ClawHub release page](https://clawhub.ai/billchen1020/verilog-design) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with Verilog/SystemVerilog code blocks, shell commands, and diagnostic guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create workspace HDL, testbench, simulation log, VVP, and VCD files when the agent follows the workflow.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
