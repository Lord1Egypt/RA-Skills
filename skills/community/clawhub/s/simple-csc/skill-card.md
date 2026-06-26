## Description: <br>
Guides developers through using the simple-csc repository for Chinese Spelling Correction and Chinese Character Error Correction with large language models in a training-free workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jacob-Zhou](https://clawhub.ai/user/Jacob-Zhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up and operate simple-csc for Chinese text correction, including local environment setup, LMCorrector API usage, REST API serving, batch experiments, and evaluation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Referenced setup scripts and dataset/model downloads come from an external repository rather than bundled code. <br>
Mitigation: Review the external repository before execution and run setup inside an isolated virtual environment. <br>
Risk: The REST API server can expose text correction endpoints if bound beyond localhost. <br>
Mitigation: Keep the service bound to 127.0.0.1 unless intentional network exposure has been reviewed and secured. <br>
Risk: Large language model execution may require substantial GPU memory and compatible CUDA support. <br>
Mitigation: Confirm NVIDIA GPU, CUDA, Python version, and VRAM requirements before deployment. <br>


## Reference(s): <br>
- [Simple CSC ClawHub page](https://clawhub.ai/Jacob-Zhou/simple-csc) <br>
- [Simple CSC repository](https://github.com/Jacob-Zhou/simple-csc) <br>
- [Detailed reference](references/details.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline Python, shell, JSON, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include localhost API examples, setup commands, model selection guidance, dataset and evaluation instructions, and cautions for external repository scripts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
