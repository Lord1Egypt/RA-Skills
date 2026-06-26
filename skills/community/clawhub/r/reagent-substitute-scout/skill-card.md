## Description: <br>
Find validated alternative reagents based on literature citation data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, lab staff, and scientific workflow developers use this skill to look up candidate substitute reagents by name, CAS number, or formula and review ranked alternatives with citation-oriented evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reagent queries and optional PubMed API credentials may be sent to external NCBI, PubChem, or chemistry data services. <br>
Mitigation: Use only non-confidential compound names or project details unless organizational policy permits external database lookups. <br>
Risk: Suggested substitutes depend on public literature and database availability and may be incomplete for specialized reagents. <br>
Mitigation: Treat results as decision support and verify candidate substitutes against laboratory requirements before use. <br>
Risk: The skill can write result files to a user-provided path. <br>
Mitigation: Choose output paths deliberately and avoid locations that could expose sensitive reagent searches or project context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/reagent-substitute-scout) <br>
- [Publisher Profile](https://clawhub.ai/user/aipoch-ai) <br>
- [Audit Reference](references/audit-reference.md) <br>
- [NCBI PubMed E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils) <br>
- [ChEMBL API](https://www.ebi.ac.uk/chembl/api/data) <br>
- [PubChem PUG REST](https://pubchem.ncbi.nlm.nih.gov/rest/pug) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Table, JSON, or Markdown report with ranked reagent substitutes and supporting citation fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write results to a user-selected output path; default result limit is configurable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and script header) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
