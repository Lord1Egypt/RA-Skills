## Description: <br>
OpenClaw memory-management skill for temporary, long-term, and permanent memories with vector semantic search, automatic compression, user identity handling, and cross-device synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pupper0601](https://clawhub.ai/user/pupper0601) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to maintain structured personal and shared AI memory, search prior context semantically, summarize activity, and synchronize memory content across devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and index private memory files and synchronize memory content through GitHub. <br>
Mitigation: Use a private dedicated repository, review the remote URL before syncing, and avoid storing secrets or highly sensitive personal data in the memory repository. <br>
Risk: Installation and configuration may persist environment variables or other settings in shell startup files. <br>
Mitigation: Prefer manual installation or the no-shell-rc option, and manage API keys outside shell startup files when possible. <br>
Risk: One-line curl-to-bash installation executes downloaded code immediately. <br>
Mitigation: Download and inspect the installer before running it, or install dependencies and configuration manually. <br>
Risk: Embedding backends may send memory text to external API providers. <br>
Mitigation: Use only trusted providers and switch to keyword-only or local workflows for sensitive memories. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pupper0601/pupper0601-memory-manager) <br>
- [Publisher Profile](https://clawhub.ai/user/pupper0601) <br>
- [README](README.md) <br>
- [Memory Style Guide](MEMORY_STYLE_GUIDE.md) <br>
- [Reference](reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command-line examples and memory-file conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory files, invoke embedding providers, and synchronize memory content through Git-backed workflows.] <br>

## Skill Version(s): <br>
v3.5.5 (source: server release metadata; artifact SKILL.md and pyproject.toml report 3.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
