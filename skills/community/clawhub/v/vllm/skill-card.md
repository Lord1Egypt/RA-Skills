## Description:

vLLM inference engine assistant for high-performance LLM deployment, PagedAttention, and OpenAI-compatible APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and operate high-throughput vLLM-based LLM serving, including installation, OpenAI-compatible API startup, GPU parallelism, model selection, quantization, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable package versions and container tags can change installed behavior over time.

Mitigation: Pin vLLM package versions and container image digests before using the commands.

Risk: The sample serving commands can expose an unauthenticated GPU-backed inference service.

Mitigation: Bind the service to localhost or a private interface unless intentionally public, and require API authentication.

Risk: Mounting a broad Hugging Face cache can expose unrelated tokens or private model artifacts.

Mitigation: Mount only the required model cache or use scoped credentials with least privilege.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tables and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may install vLLM, run containers, and start GPU-backed inference services; review and adapt before execution.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
