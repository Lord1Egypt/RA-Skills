## Description: <br>
Comprehensive SMILES profiling through SwissTargetPrediction, PubChem, ADMETlab 3.0, ChEMBL, and PK-Smart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hendr15k](https://clawhub.ai/user/hendr15k) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and cheminformatics users can profile a single SMILES string to collect identity, physicochemical, predicted target, analog, ADMET, and pharmacokinetic context from named chemistry services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SMILES strings submitted through the skill may be sent to third-party chemistry services. <br>
Mitigation: Use only compound structures that your organization permits you to share with those external services; avoid confidential, unpublished, proprietary, or regulated structures unless approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hendr15k/smiles-profiling) <br>
- [SwissTargetPrediction](https://www.swisstargetprediction.ch/) <br>
- [ADMETlab 3.0](https://admetlab3.scbdd.com/) <br>
- [ADMETlab 3.0 OpenAPI](https://admetlab3.scbdd.com/api/openapi.json) <br>
- [PubChem PUG REST](https://pubchem.ncbi.nlm.nih.gov/rest/pug) <br>
- [ChEMBL Data Web Services](https://www.ebi.ac.uk/chembl/api/data) <br>
- [PK-Smart Single SMILES](https://pk-predictor.serve.scilifelab.se/PKSmart_Single_SMILES) <br>
- [endpoints.md](references/endpoints.md) <br>
- [tool-notes.md](references/tool-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown report with tool-specific sections and optional JSON-like structured data from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports preserve tool names, units, thresholds, misses, and graceful failure notes when a source is unavailable.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
