## Description: <br>
Query and annotate gene variants from ClinVar and dbSNP databases, returning clinical significance, ACMG classification, allele frequency, and disease association information. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and bioinformatics users can use this skill to query individual or batch genetic variants and summarize public database annotations for research or educational review. It is not a diagnostic tool and clinical interpretation should be reviewed by qualified genetics professionals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried variant data may be sent to NCBI services during annotation. <br>
Mitigation: Use only data appropriate for external API queries, avoid broad or sensitive input files, and run the skill in a sandboxed workspace. <br>
Risk: The skill presents simplified clinical classifications and interpretation summaries that could be mistaken for diagnostic guidance. <br>
Mitigation: Use outputs for research or education only and have any clinical interpretation reviewed by qualified genetics professionals using current authoritative sources. <br>
Risk: Batch mode and configurable output paths can write annotation results to local files. <br>
Mitigation: Choose output paths carefully, keep generated files in the intended workspace, and avoid storing sensitive variant data unnecessarily. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/AIPOCH-AI/variant-annotation) <br>
- [ACMG/AMP Guidelines for Variant Classification](references/acmg-guidelines.md) <br>
- [ClinVar Database Guide](references/clinvar-guide.md) <br>
- [HGVS Nomenclature Guide](references/hgvs-nomenclature.md) <br>
- [Example Variants for Testing](references/example-variants.md) <br>
- [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/) <br>
- [HGVS Variant Nomenclature](https://varnomen.hgvs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, files, guidance] <br>
**Output Format:** [JSON or plain text variant annotation summaries; CLI output can also be written to a JSON file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ClinVar clinical significance, ACMG criteria and score, disease associations, population frequencies, HGVS identifiers, and interpretation summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
