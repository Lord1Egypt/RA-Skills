## Description:

Find validated alternative reagents based on literature citation data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, lab operations teams, and scientific developers use this skill to identify reagent substitutes from reagent names, CAS numbers, or molecular formulas and generate reviewable reports based on literature and chemical data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The output option can overwrite arbitrary writable files.

Mitigation: Restrict output to a new file inside the workspace and review paths before execution.

Risk: Install dependencies are not pinned.

Mitigation: Install in a dedicated virtual environment, pin versions, and audit dependencies before use.

Risk: Reagent names, CAS numbers, or research programs may be sent to external PubMed or PubChem services.

Mitigation: Use only with approved network egress and non-confidential inputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/reagent-substitute-scout)
- [Audit Reference](references/audit-reference.md)
- [PubMed E-utilities API](https://eutils.ncbi.nlm.nih.gov/entrez/eutils)
- [ChEMBL API](https://www.ebi.ac.uk/chembl/api/data)
- [PubChem PUG REST API](https://pubchem.ncbi.nlm.nih.gov/rest/pug)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Table text, JSON, or Markdown reagent substitute report with optional shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write reports to a specified output path; results may depend on API availability, API keys, RDKit support, and public literature coverage.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
