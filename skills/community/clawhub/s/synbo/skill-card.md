## Description: <br>
Bayesian optimization for chemical reactions using the synbo package, including reaction-space setup, descriptor generation, optimization, recommended-condition export, and result upload workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boeingart](https://clawhub.ai/user/boeingart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, chemists, and research engineers use this skill to prepare reaction inputs, generate descriptors, run SynBO initial sampling or Bayesian optimization, and review recommended experimental conditions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and updates local project files, including reaction-space, descriptor, optimization-settings, and results files. <br>
Mitigation: Verify the project directory before running the workflow, keep backups of existing reaction results, and review generated files before using them for experiments. <br>
Risk: The workflow includes Miniconda and pip package installation steps. <br>
Mitigation: Review the installation commands and package sources before executing them in the target environment. <br>


## Reference(s): <br>
- [SynBO Skill](https://clawhub.ai/boeingart/synbo) <br>
- [Installation Guide](reference/installation.md) <br>
- [Condition Descriptors](reference/get_desc.md) <br>
- [Initialize](reference/initialize.md) <br>
- [Optimize](reference/optimize.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, CSV descriptor files, and CSV or Excel recommendation files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes project configuration, descriptor, reaction-space, and results files in the user-selected project directory.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
