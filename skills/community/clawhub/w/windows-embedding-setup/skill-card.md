## Description:

Helps agents guide Windows users through configuring OpenClaw local embedding and memory retrieval with a local GGUF model, local memorySearch provider settings, restart checks, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dnaxxx-hub](https://clawhub.ai/user/dnaxxx-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to set up local memory embedding on Windows, including downloading the nomic embed GGUF model, configuring openclaw.json, installing the required local runtime dependency, and verifying behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing unpinned native npm code into the OpenClaw application directory can introduce dependency or binary supply-chain risk.

Mitigation: Use a pinned and reviewed node-llama-cpp version or lockfile before installation.

Risk: Ignoring high or critical npm vulnerability reports can leave the local OpenClaw runtime exposed to known issues.

Mitigation: Review npm vulnerability output and resolve high or critical findings before relying on the setup.

Risk: Loading an unverified downloaded GGUF model can introduce integrity or provenance uncertainty.

Mitigation: Verify the GGUF model using a trusted hash or immutable release before loading it.

Risk: Incorrect Windows paths or configuration edits can prevent local memory retrieval from activating.

Mitigation: Confirm escaped Windows paths, provider settings, full application restart, and the provided verification output.

## Reference(s):

- [Windows local embedding setup reference](references/windows-setup.md)
- [nomic-embed-text-v1.5 GGUF model page](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF)
- [nomic-embed-text-v1.5.Q8_0.gguf download](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF/resolve/main/nomic-embed-text-v1.5.Q8_0.gguf)
- [ClawHub skill page](https://clawhub.ai/dnaxxx-hub/skills/windows-embedding-setup)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with PowerShell, JavaScript, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend local file downloads, npm installation, OpenClaw configuration edits, application restart, and verification commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
