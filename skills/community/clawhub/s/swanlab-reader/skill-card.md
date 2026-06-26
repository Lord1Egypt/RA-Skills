## Description: <br>
读取 SwanLab 实验数据。当用户发来 SwanLab run URL 时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckqiao](https://clawhub.ai/user/ckqiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect SwanLab projects and runs, review run configuration, retrieve metric histories, plot metric trends, and compare multiple runs from SwanLab URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access SwanLab data available to the configured API key. <br>
Mitigation: Use a SwanLab API key with only the permissions needed for the intended project or run. <br>
Risk: Using set-key stores the SwanLab API key in a local plaintext file. <br>
Mitigation: Prefer temporary environment variables, or restrict permissions on ~/.config/swanlab/key when file storage is required. <br>
Risk: The skill depends on swanlab and numpy packages. <br>
Mitigation: Review dependency sources and versions before use in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckqiao/swanlab-reader) <br>
- [SwanLab platform](https://swanlab.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text with tabular summaries, metric values, suggested shell commands, and optional ASCII plots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SWANLAB_KEY or SWANLAB_API_KEY for private SwanLab data access; can also store a key in ~/.config/swanlab/key when the set-key command is used.] <br>

## Skill Version(s): <br>
1.1.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
