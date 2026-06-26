## Description: <br>
Production-ready vLLM deployment on AMD ROCm GPUs. Combines environment auto-check, model parameter detection, Docker Compose deployment, health verification, and functional testing with comprehensive logging and security best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexhegit](https://clawhub.ai/user/alexhegit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and platform engineers use this skill to deploy Hugging Face models with vLLM on AMD ROCm GPU hosts, including environment checks, Docker Compose configuration, health checks, functional tests, and deployment reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hugging Face tokens may be partially exposed and deployment logs or reports may contain sensitive deployment details. <br>
Mitigation: Use a least-privilege token, avoid persistent shell-profile storage when possible, and redact DEPLOYMENT_REPORT.md, deployment.log, and test-results.json before sharing. <br>
Risk: The default Docker image is a nightly tag, which can change between deployments. <br>
Mitigation: Pin the Docker image to a reviewed version or digest before production use. <br>
Risk: The deployment workflow is intended to run host-level Docker and ROCm checks on systems with GPU device access. <br>
Mitigation: Install and run it only on a dedicated ROCm deployment host with reviewed Docker, GPU, and filesystem permissions. <br>


## Reference(s): <br>
- [ROCm vLLM Deployment on ClawHub](https://clawhub.ai/alexhegit/rocm-vllm-deployment) <br>
- [alexhegit publisher profile](https://clawhub.ai/user/alexhegit) <br>
- [Hugging Face token settings](https://huggingface.co/settings/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, generated Docker Compose configuration, JSON test results, logs, and deployment reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deployment artifacts are written under $HOME/vllm-compose/<model-id>/ when the skill is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
