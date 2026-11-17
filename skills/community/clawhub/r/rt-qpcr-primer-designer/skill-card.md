## Description:

Helps researchers design and assess candidate RT-qPCR primer pairs from GenBank accessions or FASTA sequences and prepare an Excel report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zd200572](https://clawhub.ai/user/zd200572)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and laboratory staff use the skill to draft SYBR Green RT-qPCR primers, compare thermodynamic properties, and prepare candidate reports for independent experimental review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Specificity results may be mistaken for BLAST or transcriptome validation even though the included script does not perform those checks.

Mitigation: Independently verify primer specificity with a trusted BLAST or transcriptome workflow before experimental use.

Risk: Accession lookups contact NCBI and report generation writes files to disk.

Mitigation: Confirm network use before lookups and choose explicit output paths.

## Reference(s):

- [RT-qPCR primer design principles](references/qpcr_principles.md)
- [Teleost reference genes](references/teleost_housekeeping_genes.md)
- [ClawHub skill release](https://clawhub.ai/zd200572/skills/rt-qpcr-primer-designer)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Markdown guidance and Excel (.xlsx) primer report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranked primer candidates and experimental guidance; specificity is not BLAST- or transcriptome-validated.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
