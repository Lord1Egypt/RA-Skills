## Description: <br>
Pack and analyze codebases into AI-friendly single files using Repomix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yamadashy](https://clawhub.ai/user/yamadashy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to package local directories or remote GitHub repositories into AI-friendly files, inspect repository structure, search for code patterns, and estimate token counts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Packaging repositories for AI analysis can expose private or proprietary code through generated output files. <br>
Mitigation: For sensitive repositories, narrow scope with include or ignore filters, avoid secret-bearing directories, review generated output before sharing it, and delete temporary analysis files when finished. <br>
Risk: Using the latest npm package at execution time may introduce unreviewed behavior changes. <br>
Mitigation: Pin the Repomix npm package version when reproducibility or tighter change control is required. <br>


## Reference(s): <br>
- [Repomix GitHub Repository](https://github.com/yamadashy/repomix) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces repository packaging commands, analysis guidance, and reporting suggestions; generated Repomix output files may be XML, Markdown, plain text, or JSON depending on selected CLI options.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
