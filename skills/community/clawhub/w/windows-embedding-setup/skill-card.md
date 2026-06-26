## Description: <br>
Guides an agent through setting up local OpenClaw memory embeddings on Windows, including downloading the GGUF model, installing the local runtime dependency, editing configuration, restarting OpenClaw, and verifying status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dnaxxx-hub](https://clawhub.ai/user/dnaxxx-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure local memory retrieval embeddings on Windows and diagnose common setup failures such as missing dependencies, incorrect paths, inactive local provider settings, or incomplete restarts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup downloads a model file and installs node-llama-cpp from external sources. <br>
Mitigation: Confirm the Hugging Face model URL and npm package are trusted before running the commands. <br>
Risk: The setup changes a local OpenClaw installation and its openclaw.json configuration. <br>
Mitigation: Back up openclaw.json and run commands only in the intended OpenClaw installation. <br>
Risk: Application updates may overwrite files changed inside bundled OpenClaw resources. <br>
Mitigation: Recheck the local embedding dependency and memory status after OpenClaw updates. <br>


## Reference(s): <br>
- [Windows local embedding setup guide](references/windows-setup.md) <br>
- [nomic-embed-text-v1.5 GGUF model card](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with PowerShell, JavaScript, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces procedural guidance for local Windows setup and verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
