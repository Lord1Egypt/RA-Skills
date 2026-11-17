## Description:

A skill for performing sequence alignment using NCBI BLAST API. Supports nucleotide and protein sequence comparison against major biological databases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and bioinformatics users can use this skill to run BLAST sequence similarity searches for nucleotide or protein queries and review alignment results against supported biological databases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill submits user-provided biological sequences to NCBI's external BLAST service.

Mitigation: Do not submit unpublished, proprietary, regulated, or sample-identifying sequence data unless external submission to NCBI is approved.

Risk: The script can write returned alignment results to the output path supplied by the user.

Mitigation: Choose output paths deliberately and keep generated files within the intended workspace.

## Reference(s):

- [BLAST Documentation](references/blast_docs.md)
- [NCBI BLAST API Guide](references/ncbi_api_guide.md)
- [NCBI BLAST Help](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs)
- [NCBI BLAST API Endpoint](https://blast.ncbi.nlm.nih.gov/Blast.cgi)
- [NCBI Policies](https://www.ncbi.nlm.nih.gov/home/about/policies/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and BLAST result outputs in text, JSON, or CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write alignment results to a user-specified output path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
