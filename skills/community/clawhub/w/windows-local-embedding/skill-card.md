## Description: <br>
Guides Windows users through configuring OpenClaw local embedding and local memory search with a GGUF model, local provider settings, status checks, and setup troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dadaniya99](https://clawhub.ai/user/dadaniya99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users on Windows use this skill to set up local memory embeddings with nomic-embed-text-v1.5.Q8_0.gguf, configure memorySearch.provider to local, and verify or troubleshoot the setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing node-llama-cpp introduces normal npm dependency and package-installation risk. <br>
Mitigation: Verify the package before running npm install and review warnings instead of ignoring them. <br>
Risk: Editing openclaw.json can break local memory search if the JSON structure or Windows path escaping is wrong. <br>
Mitigation: Back up openclaw.json before editing, validate the provider and modelPath values, and fully restart OpenClaw after changes. <br>
Risk: A wrong or incomplete model download can make local embeddings fail. <br>
Mitigation: Confirm the model comes from the stated Hugging Face source and verify the GGUF file header and expected file size. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dadaniya99/windows-local-embedding) <br>
- [Windows setup reference](references/windows-setup.md) <br>
- [nomic-embed-text-v1.5-GGUF model page](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF) <br>
- [nomic-embed-text-v1.5.Q8_0.gguf download](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF/resolve/main/nomic-embed-text-v1.5.Q8_0.gguf) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with PowerShell, JSON, and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows-specific setup guidance for OpenClaw local memory search.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
