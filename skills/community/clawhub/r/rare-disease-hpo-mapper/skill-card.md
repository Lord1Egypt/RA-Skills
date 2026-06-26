## Description: <br>
Map patient symptoms to Human Phenotype Ontology terms for gene diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to map comma-separated symptom descriptions to a small, local set of HPO term suggestions for rare disease review workflows. It is best treated as bounded terminology assistance, not as a comprehensive clinical decision system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may over-rely on a small local lookup as clinical decision support. <br>
Mitigation: Use the skill only as terminology assistance and review outputs against appropriate clinical, ontology, and diagnostic workflows before acting on them. <br>
Risk: Symptom inputs can contain patient-identifying health information. <br>
Mitigation: Avoid entering real patient-identifying health information unless the execution environment is approved for that data. <br>
Risk: The packaged requirements file declares difflib even though it is part of the Python standard library. <br>
Mitigation: Review dependencies before installation and remove the unnecessary difflib entry if using pip-based setup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/rare-disease-hpo-mapper) <br>
- [Publisher profile](https://clawhub.ai/user/aipoch-ai) <br>
- [Audit Reference](references/audit-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and plain-text HPO mapping results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include matched symptom text, HPO identifiers, HPO names, and simple confidence labels when the packaged script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
