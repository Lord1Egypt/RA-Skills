## Description:

Map patient symptoms to Human Phenotype Ontology terms for gene diagnosis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to map patient symptom descriptions to HPO term suggestions for rare disease diagnosis, genetic counseling, cohort building, and related genetic analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security review reports an unnecessary unpinned dependency entry in requirements.txt that may create avoidable supply-chain risk.

Mitigation: Review dependencies before installation and remove the difflib requirements entry or skip pip install -r requirements.txt unless a reviewed dependency file is provided.

Risk: Patient symptom descriptions may contain sensitive health information, and HPO suggestions may be clinically incorrect or incomplete.

Mitigation: Handle patient inputs as sensitive health data and require clinical review before using mapped HPO terms for diagnosis, counseling, or research decisions.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/rare-disease-hpo-mapper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with optional shell commands and text mapping results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The packaged script prints symptom-to-HPO mapping results with confidence labels; users should clinically verify HPO suggestions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
