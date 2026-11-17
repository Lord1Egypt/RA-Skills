## Description:

Install and configure vLLM-Plugin-FL for multiple hardware backends, including NVIDIA, Ascend, MetaX, Iluvatar, and Moore Threads, with dependency setup, backend configuration, troubleshooting, and inference verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wbavon](https://clawhub.ai/user/wbavon)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to set up vLLM-Plugin-FL, FlagGems, and optional FlagCX across supported accelerator backends, then verify the environment with a local inference test.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and builds external source repositories and changes the Python environment.

Mitigation: Install in a disposable container or dedicated virtual environment, review cloned repositories and build files before execution, and prefer pinned commits or verified package hashes.

Risk: The quick test can perform a broad filesystem search for model directories.

Mitigation: Ask for explicit approval before broad searches and prefer user-provided model paths or constrained search locations.

Risk: Proxy configuration can expose credential-bearing proxy URLs.

Mitigation: Avoid sharing proxy URLs that contain credentials and redact secrets from terminal output and logs.

## Reference(s):

- [vLLM v0.13.0](https://github.com/vllm-project/vllm/tree/v0.13.0)
- [vLLM-FL fork](https://github.com/flagos-ai/vllm-FL)
- [vLLM-Plugin-FL GitHub](https://github.com/flagos-ai/vllm-plugin-FL)
- [FlagGems GitHub](https://github.com/flagos-ai/FlagGems)
- [FlagCX GitHub](https://github.com/flagos-ai/FlagCX)
- [Additional Steps for Ascend NPU](references/npu.md)
- [Additional Steps for Iluvatar GPU](references/iluvatar_gpu.md)
- [Additional Steps for Moore Threads GPU](references/mthreads_gpu.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, environment variables, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may modify Python environments, clone external repositories, build native extensions, and search local filesystem paths during verification.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
