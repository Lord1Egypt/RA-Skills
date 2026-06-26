## Description: <br>
Use Siemens TIA Portal Openness API to diff two .zap18 projects and return structured code and hardware changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjmore66](https://clawhub.ai/user/cjmore66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to compare baseline and new Siemens TIA Portal .zap18 projects and explain structured code, block, and hardware changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may invoke a local TIA Openness diff script that reads and writes project-related files. <br>
Mitigation: Review and trust the provided PowerShell or batch script before use, restrict inputs to intended .zap18 files, and run it in a controlled working directory. <br>
Risk: Generated diff output can expose sensitive engineering details. <br>
Mitigation: Treat JSON and Markdown diff outputs as sensitive project artifacts and share them only through approved channels. <br>


## Reference(s): <br>
- [TIA Openness Diff Scripts](Scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON summaries and human-readable Markdown explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file paths, timestamps, and counts of added, removed, or modified blocks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
