## Description: <br>
Full memory stack for OpenClaw on Windows. Includes LanceDB semantic memory, git-notes decision memory, and memory hygiene workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sea2049](https://clawhub.ai/user/Sea2049) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to add persistent memory to OpenClaw on Windows, including LanceDB-backed semantic recall, branch-aware git-notes decision memory, and maintenance guidance for memory quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store and reuse user or project context silently in local memory. <br>
Mitigation: Use it only in repositories where silent local memory is acceptable, disable or limit auto-capture when appropriate, and avoid storing secrets or regulated data. <br>
Risk: The git-notes workflow can modify repository metadata. <br>
Mitigation: Review git-notes commands before use and run them only in repositories where git metadata changes are acceptable. <br>
Risk: The memory hygiene workflow includes wipe commands that can delete local memory data. <br>
Mitigation: Back up important memory data and confirm storage paths before running cleanup or wipe commands. <br>
Risk: The LanceDB backend depends on third-party Python packages. <br>
Mitigation: Pin and audit dependencies before installing them in production or sensitive environments. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/Sea2049/vector-memory-windows) <br>
- [Memory Hygiene reference](https://github.com/xdylanbaker/memory-hygiene) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python APIs, JSON examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or modifies local LanceDB storage and git notes when an agent follows the workflows; destructive cleanup commands require review.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact/clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
