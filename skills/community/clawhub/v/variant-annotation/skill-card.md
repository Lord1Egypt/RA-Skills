## Description:

Variant Annotation queries and interprets genetic variants from ClinVar and dbSNP, returning clinical significance, ACMG-style classification, population frequencies, disease associations, and functional predictions.

This skill is for research and development only.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers, bioinformatics analysts, and research users use this skill to query rsID, HGVS, VCF-style, or coordinate inputs and summarize variant significance, population data, disease associations, and ACMG-style evidence. Outputs require expert review and are not diagnostic advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Variant identifiers may be sent to NCBI services during annotation.

Mitigation: Avoid patient-identifying data, use the minimum necessary variant information, and only provide an NCBI API key when needed.

Risk: Algorithmic ACMG-style classifications can overstate pathogenicity, especially when population data is missing.

Mitigation: Treat classifications as research support only and require review by qualified genetics professionals before clinical use.

Risk: Outputs may be persisted wherever the user chooses to write result files.

Mitigation: Run in an isolated environment and write results only to approved storage locations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/variant-annotation)
- [ACMG/AMP Guidelines for Variant Classification](references/acmg-guidelines.md)
- [ClinVar Database Guide](references/clinvar-guide.md)
- [HGVS Nomenclature Guide](references/hgvs-nomenclature.md)
- [Example Variants for Testing](references/example-variants.md)
- [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/)
- [HGVS Variant Nomenclature](https://varnomen.hgvs.org/)
- [Mutalyzer](https://mutalyzer.nl/)
- [VariantValidator](https://variantvalidator.org/)
- [ClinGen Allele Registry](https://reg.clinicalgenome.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON or plain-text variant annotation outputs and optional Python or shell snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query external variant databases and write user-selected result files.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
