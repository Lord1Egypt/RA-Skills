## Description:

Guides Windows users through configuring OpenClaw to use local memory search embeddings with the nomic-embed-text-v1.5 GGUF model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dadaniya99](https://clawhub.ai/user/dadaniya99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users on Windows use this skill to install local embedding support, configure memorySearch.provider as local, verify GGUF model loading, and troubleshoot path, restart, provider, or dependency issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs native node-llama-cpp code into OpenClaw without pinning a package version.

Mitigation: Use a pinned node-llama-cpp version, review npm warnings and vulnerability output, and install only in an environment where modifying OpenClaw application files is acceptable.

Risk: The model download is referenced without a pinned revision or full SHA-256 verification.

Mitigation: Download the model from a trusted pinned revision and verify a full SHA-256 hash before configuring OpenClaw to load it.

Risk: Manual Windows path and application-file changes can prevent local embeddings from loading if configuration is malformed or OpenClaw is not fully restarted.

Mitigation: Validate JSON structure and escaped Windows paths, fully restart OpenClaw, and run the provided status check before relying on local memory search.

## Reference(s):

- [Windows local embedding setup](references/windows-setup.md)
- [nomic-embed-text-v1.5-GGUF model page](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF)
- [nomic-embed-text-v1.5.Q8_0.gguf download](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF/resolve/main/nomic-embed-text-v1.5.Q8_0.gguf)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with PowerShell, JavaScript, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides step-by-step Windows setup and troubleshooting guidance for local OpenClaw memory search embeddings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
