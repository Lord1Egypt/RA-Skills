## Description: <br>
Query and annotate gene variants from ClinVar and dbSNP databases with ACMG guideline support. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[EC-cyber258](https://clawhub.ai/user/EC-cyber258) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and bioinformatics users can query rsID, HGVS, VCF-style, or genomic-coordinate variants to receive ClinVar/dbSNP annotations, ACMG-style classifications, population-frequency context, disease associations, and interpretation summaries. The skill is for research and educational variant review, not clinical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Variant identifiers or related genomic inputs may be sent to external NCBI services for lookup. <br>
Mitigation: Use only with data that users are comfortable sending to NCBI, and avoid full VCF or identifiable genomic data unless consent and data-minimization controls are in place. <br>
Risk: ACMG and pathogenicity outputs are algorithmic and may be misleading if treated as medical advice. <br>
Mitigation: Require review by a qualified genetics professional before using clinically meaningful results. <br>
Risk: External database lookups can be incomplete, rate-limited, stale, or unavailable. <br>
Mitigation: Check source review status and recency, handle API failures explicitly, and do not rely on a single automated lookup for consequential decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/EC-cyber258/variant-annotation-2) <br>
- [Publisher profile](https://clawhub.ai/user/EC-cyber258) <br>
- [ACMG/AMP Guidelines for Variant Classification](references/acmg-guidelines.md) <br>
- [ClinVar Database Guide](references/clinvar-guide.md) <br>
- [Example Variants for Testing](references/example-variants.md) <br>
- [HGVS Nomenclature Guide](references/hgvs-nomenclature.md) <br>
- [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/) <br>
- [HGVS Nomenclature](https://varnomen.hgvs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional Python, shell, JSON, or plain-text variant annotation output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read variant lists from files and write JSON output files when invoked through the bundled script.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
