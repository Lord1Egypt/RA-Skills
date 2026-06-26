## Description: <br>
Offline local semantic code search using embeddings to find and index code by meaning with llama.cpp, ONNX, or Ollama backends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rizperdana](https://clawhub.ai/user/rizperdana) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to index local projects and search code by semantic meaning rather than exact keywords. It is intended for offline-capable code discovery workflows using local embedding backends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may search or index local project files when enabled with broad triggers. <br>
Mitigation: Narrow activation triggers and enable it only for repositories or project paths intended for semantic indexing. <br>
Risk: The documentation includes an embedded installation token. <br>
Mitigation: Do not reuse embedded tokens from documentation; install through a trusted ClawHub flow or a freshly issued token. <br>
Risk: Install instructions and activation scope require human review before deployment. <br>
Mitigation: Review the README and installer files before installation, then scan the installed package in the target environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rizperdana/semantic-grep) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON or agent installer snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Offline-capable local code indexing and search guidance; command execution and project-file access depend on the host agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
