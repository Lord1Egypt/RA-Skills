## Description: <br>
Automates SAUSG structural analysis workflows, including opening SAUSG modules, running structural calculations, and reading calculation results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiasu1017-beep](https://clawhub.ai/user/jiasu1017-beep) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Structural engineers and developers use this skill to operate local SAUSG installations, run nonlinear or dynamic structural calculations, and summarize key model result files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The calculation workflow can delete old result files and result folders in the selected model directory by default. <br>
Mitigation: Back up project folders first and use --no-cleanup unless cleanup is intended. <br>
Risk: The scripts start local SAUSG executables with user-provided model and installation paths. <br>
Mitigation: Install only in trusted local SAUSG environments and avoid untrusted model or SAUSG paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiasu1017-beep/sausg) <br>
- [SAUSG product page](https://product.pkpm.cn/productDetails?productId=56) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and text analysis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start local SAUSG executables, inspect model result files, and delete prior result files unless run with --no-cleanup.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
