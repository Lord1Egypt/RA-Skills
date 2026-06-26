## Description: <br>
Saturnday provides governed AI software execution with deterministic governance checks, LLM-assisted security triage, AI-backed build workflows, governed document generation, release preflight inspection, and auto-repair. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[honouralexwill](https://clawhub.ai/user/honouralexwill) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to scan skills and repositories, run governance checks before merge or deployment, build projects from briefs under per-commit governance, create governed documents, inspect release artifacts, and repair findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Run, guard, and repair modes can modify the target repository through commits, generated evidence, and related workflow files. <br>
Mitigation: Use these modes only on intended repositories with a clean git state, backup, or disposable branch; use scan mode for lower-impact review. <br>
Risk: AI-backed run mode can transmit repository contents to the selected backend provider. <br>
Mitigation: Choose an explicit approved backend and avoid running it on confidential or regulated code unless that provider is authorized for the data. <br>
Risk: The skill depends on installing and executing the external Saturnday package. <br>
Mitigation: Install only when you trust the package source and verify the installed Saturnday version before use. <br>


## Reference(s): <br>
- [ClawHub Saturnday skill page](https://clawhub.ai/honouralexwill/saturnday) <br>
- [Saturnday homepage](https://www.saturnday.dev) <br>
- [Saturnday skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON results from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Run and guard workflows may create governance evidence, reports, progress logs, plans, and commits in the target repository.] <br>

## Skill Version(s): <br>
1.8.1 (source: server release evidence; artifact frontmatter reports 1.8.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
