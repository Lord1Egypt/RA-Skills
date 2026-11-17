## Description:

Queries and annotates gene variants from ClinVar and dbSNP databases with clinical significance, ACMG classification, allele frequency, disease association, and functional prediction outputs.

This skill is for research and development only.

## Publisher:

[ec-cyber258](https://clawhub.ai/user/ec-cyber258)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and bioinformatics users can use this skill to annotate rsID, HGVS, genomic-coordinate, VCF-style, or gene amino-acid variant inputs for research-oriented interpretation. Outputs should be treated as provisional and not used for diagnosis or treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Variant identifiers and batch files may contain sensitive genetic information and can be transmitted to external NCBI services.

Mitigation: Review inputs for sensitivity before use, avoid submitting protected or confidential genetic data, and use only approved environments for research workflows.

Risk: ACMG-style classifications are provisional and evidence notes identify a medical-classification flaw when population data is missing.

Mitigation: Do not use outputs for diagnosis or treatment; require review by qualified genetics professionals and validate results against authoritative clinical laboratory sources.

Risk: Command-line API keys can be exposed through shell history, process listings, or logs.

Mitigation: Avoid passing valuable API keys directly on the command line; prefer approved secret-handling mechanisms and rotate credentials if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ec-cyber258/skills/variant-annotation-2)
- [ACMG/AMP Guidelines for Variant Classification](references/acmg-guidelines.md)
- [ClinVar Database Guide](references/clinvar-guide.md)
- [HGVS Nomenclature Guide](references/hgvs-nomenclature.md)
- [Example Variants for Testing](references/example-variants.md)
- [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/)
- [HGVS Recommendations](https://varnomen.hgvs.org/)
- [ACMG Standards and Guidelines PDF](https://www.acmg.net/PDFLibrary/Standards-Guidelines-for-Interpretation-of-Sequence-Variants.pdf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python API examples, shell commands, and JSON or text variant annotation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query external NCBI services and may write JSON output files when an output path is supplied.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
