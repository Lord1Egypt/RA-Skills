## Description:

Designs high-specificity RT-qPCR primers and probes with homology mapping, high-GC optimization, TaqMan/SYBR support, and off-target specificity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjuphd](https://clawhub.ai/user/zjuphd)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to design RT-qPCR primer and probe assay candidates for human, mouse, monkey, predicted-transcript, and high-GC viral templates. It supports workflows that need exon-junction awareness, homology mapping, SYBR Green or TaqMan assay design, and optional off-target checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script makes web requests to NCBI for user-provided accession IDs.

Mitigation: Review accession IDs before execution and run in an environment where outbound network access to NCBI is expected.

Risk: The Python dependency is listed without a pinned version.

Mitigation: Pin requests to a reviewed version or install from a lockfile before deployment.

Risk: Primer and probe candidates can be unsuitable if source annotations, homology mapping, or off-target inputs are incomplete.

Mitigation: Review the generated assay sets for Tm, GC content, 3-prime quality, gDNA safety, and specificity before laboratory use.

## Reference(s):

- [RT-qPCR Primer Design Guidelines](artifact/references/guidelines.md)
- [ClawHub skill page](https://clawhub.ai/zjuphd/skills/rtqpcr-primer-design)
- [NCBI E-utilities efetch FASTA endpoint used by the skill](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={accession}&rettype=fasta&retmode=text)
- [NCBI E-utilities efetch GenBank endpoint used by the skill](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={accession}&rettype=gb&retmode=text)

## Skill Output:

**Output Type(s):** [JSON, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON assay candidate data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assay candidates include amplicon size, forward and reverse primer sequences, melting temperatures, and optional probe data.]

## Skill Version(s):

5.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
