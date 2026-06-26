## Description: <br>
vLLM inference assistant for high-performance LLM deployment, PagedAttention, and OpenAI-compatible API serving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangifonly](https://clawhub.ai/user/zhangifonly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to get practical guidance for deploying and tuning vLLM inference servers, including OpenAI-compatible serving, GPU memory settings, model choices, quantization, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unpinned vLLM packages or Docker images can change behavior across installs. <br>
Mitigation: Pin package and container image versions before using generated setup commands in production. <br>
Risk: Mounting a broad Hugging Face cache into a container can expose more local model data than intended. <br>
Mitigation: Mount only the cache paths required for the selected model and deployment. <br>
Risk: An OpenAI-compatible API server exposed on port 8000 can be accessed by unauthorized clients if deployed without network controls. <br>
Mitigation: Bind the service behind appropriate authentication, firewall rules, and private networking before exposing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangifonly/vllm) <br>
- [Publisher profile](https://clawhub.ai/user/zhangifonly) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no tools, MCP servers, or credential environment variables are declared.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
