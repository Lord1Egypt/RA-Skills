## Description:

Production-ready vLLM deployment on AMD ROCm GPUs. Combines environment auto-check, model parameter detection, Docker Compose deployment, health verification, and functional testing with comprehensive logging and security best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexhegit](https://clawhub.ai/user/alexhegit)

### License/Terms of Use:


## Use Case:

Developers and platform engineers use this skill to deploy and verify vLLM inference services on AMD ROCm GPU hosts with Docker Compose, including environment checks, model configuration, health checks, functional tests, and deployment reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential exposure or persistence through HF_TOKEN handling.

Mitigation: Prefer command-scoped token passing, avoid storing tokens in shell startup files or deployment reports, and review generated files before sharing.

Risk: Shell startup file sourcing may execute unexpected user-local code.

Mitigation: Review or remove shell startup sourcing behavior before production use and load only the required environment variables.

Risk: Unpinned container images and unrestricted model identifiers can change runtime behavior or create unsafe paths.

Mitigation: Use pinned and reviewed container images and restrict model IDs to safe, expected names before deployment.

## Reference(s):

- [ROCm vLLM Deployment on ClawHub](https://clawhub.ai/alexhegit/skills/rocm-vllm-deployment)
- [Hugging Face Token Settings](https://huggingface.co/settings/tokens)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, Docker Compose, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deployment logs, functional test results, Docker Compose configuration, optional environment files, and a deployment report under a per-model output directory.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
