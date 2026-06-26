## Description: <br>
Stable Diffusion 3 and SD3.5 Large on Apple Silicon with DiffusionKit's MLX-native backend, Flux models through mflux and Ollama native image generation, and local routing across a device fleet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up and call local Stable Diffusion and Flux image generation through an Ollama Herd fleet router on Apple Silicon systems. It provides installation commands, API examples, monitoring commands, and guardrails for local image generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package installation and optional patch scripts can change the local Python environment or installed tools. <br>
Mitigation: Review the PyPI and uv packages and any patch script before running the setup commands. <br>
Risk: First model use can download multi-gigabyte model weights from HuggingFace. <br>
Mitigation: Plan storage and bandwidth before first use, and initiate model downloads only when ready. <br>
Risk: The local router listens on port 11435 and could expose image-generation endpoints beyond the intended machine if network access is broadened. <br>
Mitigation: Keep the router reachable only by trusted devices and networks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/stable-diffusion-sd3) <br>
- [Ollama Herd repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Image Generation Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/image-generation.md) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, curl examples, Python code, tables, and local API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local setup guidance for curl or wget, optional Python tooling, uv-installed image backends, and router usage on localhost port 11435.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
