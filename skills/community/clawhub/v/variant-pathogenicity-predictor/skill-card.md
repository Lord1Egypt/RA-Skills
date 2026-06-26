## Description: <br>
Integrates REVEL, CADD, and PolyPhen scores to predict genetic variant pathogenicity. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[EC-cyber258](https://clawhub.ai/user/EC-cyber258) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and bioinformatics practitioners can use this skill to run a local, score-based variant pathogenicity demonstration and inspect composite classification output. Results should be independently validated before clinical or research use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical genetics claims are broader than what the included code performs. <br>
Mitigation: Treat outputs as a demonstration only, and require independent validation before using results for clinical or research decisions. <br>
Risk: The artifact documentation describes VCF, variant, gene, ACMG, SIFT, and MutationTaster behavior that is not implemented by the included script. <br>
Mitigation: Use only the implemented numeric REVEL, CADD, PolyPhen, and demo arguments unless the package is updated and re-reviewed. <br>
Risk: The release is flagged suspicious by the authoritative security evidence because capability claims do not match the included code. <br>
Mitigation: Review the skill before installation and verify that documentation, CLI behavior, and intended use match the deployed artifact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EC-cyber258/variant-pathogenicity-predictor) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; the script prints plain text classification output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Python script with no external API calls according to release evidence.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
