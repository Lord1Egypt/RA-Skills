## Description: <br>
Use when one Radxa skill should cover the full offline documentation workflow: detect the current board model, map it to the correct product series, deploy or update the local MDMaker documentation mirror under ~/.openclaw/MDMaker, and query board-specific offline docs before coding, debugging, or hardware operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xzl01](https://clawhub.ai/user/xzl01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to identify Radxa hardware, map it to the correct product series, maintain a local Radxa documentation mirror, and answer board-specific documentation questions from local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deploying or updating the local documentation mirror runs external Git operations, installs Python packages, and executes build scripts under ~/.openclaw/MDMaker. <br>
Mitigation: Review the cloned repositories and build scripts before running setup, and avoid these steps on restricted or production systems unless the sources are trusted. <br>
Risk: A wrong or guessed board model can route the agent to documentation for the wrong Radxa product series. <br>
Mitigation: Use detected hardware evidence or an explicit user-provided model, and ask for clarification when the model is unknown or ambiguous. <br>
Risk: Missing local documentation could lead to unsupported answers. <br>
Mitigation: Report that the local mirror is missing unless the user explicitly asks to deploy or update it. <br>


## Reference(s): <br>
- [Device Series Map](references/device-series-map.md) <br>
- [MDMaker](https://github.com/ZIFENG278/MDMaker.git) <br>
- [Radxa Docs Source](https://github.com/radxa-docs/docs.git) <br>
- [Radxa Docs GitCode Mirror](https://gitcode.com/radxa-docs/docs.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with file paths and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May distinguish answers confirmed from local documentation from conclusions inferred from device-model mapping.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
