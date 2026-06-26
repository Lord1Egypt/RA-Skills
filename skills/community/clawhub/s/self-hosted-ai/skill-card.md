## Description: <br>
Self Hosted Ai helps agents guide users through running self-hosted LLM inference, image generation, speech-to-text, and embeddings without relying on cloud APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install, configure, and operate a self-hosted AI stack across macOS, Linux, and Windows machines. It supports local alternatives for chat completions, image generation, speech-to-text, embeddings, fleet health checks, and model recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides use of external packages and a local network service that may process confidential prompts, audio, images, or documents. <br>
Mitigation: Verify package sources, run the router only on a trusted network, and review ~/.fleet-manager logs/state before using confidential data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/self-hosted-ai) <br>
- [Ollama Herd Repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [Image Generation Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/image-generation.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>
- [Configuration Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/configuration-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, Python, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local service endpoints, package installation commands, model names, and configuration paths.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
