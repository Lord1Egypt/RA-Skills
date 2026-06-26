## Description: <br>
Qwen Qwen3 helps agents set up and use Qwen3.5, Qwen3, Qwen3-Coder, Qwen2.5-Coder, and Qwen3-ASR across a local Ollama Herd fleet for LLM inference, code generation, and speech-to-text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure local Qwen model inference, code generation, and speech-to-text through an Ollama Herd router across macOS, Linux, or Windows machines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running a local fleet router can expose prompts, source code, audio, and logs to other fleet nodes or network users if it is bound beyond trusted hosts. <br>
Mitigation: Keep the router limited to localhost or a trusted LAN, and avoid sending sensitive prompts, source code, or audio unless the operator understands where requests and logs are stored. <br>
Risk: The setup depends on local Python packages and model-serving tools that execute on the user's machines. <br>
Mitigation: Install only in environments where running the referenced Python packages and local fleet router is acceptable, and review package sources and permissions before deployment. <br>
Risk: Large Qwen models can exceed available system memory and cause failed or unstable local inference. <br>
Mitigation: Choose smaller model variants or MoE versions when available memory is insufficient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/qwen-qwen3) <br>
- [Ollama Herd repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Ollama Herd package](https://pypi.org/project/ollama-herd/) <br>
- [Agent setup guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash, Python, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance assumes a local Ollama Herd router and may reference localhost endpoints, local fleet configuration paths, and optional Python tooling.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
