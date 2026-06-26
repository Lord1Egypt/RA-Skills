## Description: <br>
Install and configure vLLM-Plugin-FL for multiple hardware backends including NVIDIA, Ascend, MetaX, Iluvatar, Moore Threads, and others. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wbavon](https://clawhub.ai/user/wbavon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install vLLM-Plugin-FL, configure FlagGems and FlagCX, apply hardware-specific setup, troubleshoot runtime issues, and verify model serving with an inference test. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask an agent to clone repositories, install Python packages, build native components, and change shell environment variables. <br>
Mitigation: Run it only in an environment where those setup actions are acceptable, and review proposed commands before execution. <br>
Risk: The quick test can search broad filesystem paths for a model directory. <br>
Mitigation: Provide an explicit local model path for testing instead of allowing a whole-machine search. <br>
Risk: Proxy setup instructions may expose sensitive proxy URLs if credentials are pasted into chat. <br>
Mitigation: Do not paste proxy URLs containing usernames, passwords, or tokens into the agent chat. <br>


## Reference(s): <br>
- [vLLM v0.13.0](https://github.com/vllm-project/vllm/tree/v0.13.0) <br>
- [vllm-FL](https://github.com/flagos-ai/vllm-FL) <br>
- [vLLM-Plugin-FL](https://github.com/flagos-ai/vllm-plugin-FL) <br>
- [FlagGems](https://github.com/flagos-ai/FlagGems) <br>
- [FlagCX](https://github.com/flagos-ai/FlagCX) <br>
- [Additional Steps for Ascend NPU](references/npu.md) <br>
- [Additional Steps for Iluvatar GPU (BI-V150)](references/iluvatar_gpu.md) <br>
- [Additional Steps for Moore Threads GPU](references/mthreads_gpu.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose repository cloning, package installation, native builds, shell environment changes, and local inference verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
