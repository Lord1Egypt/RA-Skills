## Description:

Comprehensive SMILES profiling through SwissTargetPrediction, PubChem, ADMETlab 3.0, ChEMBL, and PK-Smart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hendr15k](https://clawhub.ai/user/hendr15k)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and chemistry researchers use this skill to profile one user-provided SMILES string across target prediction, compound identity, physicochemical properties, similar compounds, ADMET signals, and pharmacokinetic estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A submitted SMILES string is sent to third-party chemistry services.

Mitigation: Use only compounds approved for those providers, and avoid confidential, proprietary, or pre-publication compounds unless their terms and retention practices are acceptable.

Risk: Remote chemistry services can be unavailable or return partial results.

Mitigation: Review tool-specific error messages and treat incomplete sections as missing evidence rather than negative findings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hendr15k/skills/smiles-profiling)
- [Endpoints](references/endpoints.md)
- [Tool Notes](references/tool-notes.md)
- [SwissTargetPrediction](https://www.swisstargetprediction.ch/)
- [ADMETlab 3.0 OpenAPI](https://admetlab3.scbdd.com/api/openapi.json)
- [PubChem PUG REST](https://pubchem.ncbi.nlm.nih.gov/rest/pug)
- [ChEMBL Data Web Services](https://www.ebi.ac.uk/chembl/api/data)
- [PK-Smart Single SMILES](https://pk-predictor.serve.scilifelab.se/PKSmart_Single_SMILES)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown report or JSON from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profiles a single SMILES string and may include partial results when a chemistry service is unavailable.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
