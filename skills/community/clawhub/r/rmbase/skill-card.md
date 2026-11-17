## Description:

Queries RMBase v3.0 for RNA modifications, sites, enzymes, interactions, motifs, and cancer-associated RNA-modifying proteins with scientific provenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo-cheung-itlger](https://clawhub.ai/user/leo-cheung-itlger)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to query and interpret RMBase v3.0 epitranscriptome records by gene, modification, species, and assembly, with retrieval provenance and optional offline dataset reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public queries and authorized uploads are sent to RMBase over unencrypted HTTP.

Mitigation: Use offline mode for private work; do not upload unpublished BED files or gene lists.

Risk: Saved responses and datasets persist locally and offline responses may be stale.

Mitigation: Review the local RMBase cache, retrieval timestamps, and dataset provenance before reuse.

Risk: Incomplete records or database associations may be mistaken for biological absence or clinical evidence.

Mitigation: Check query status, pagination, species, assembly, and cited record evidence; do not use RMBase alone for clinical decisions.

Risk: Analysis submission endpoints were unavailable during the source audit.

Mitigation: Validate inputs locally and do not promise successful remote annotation or automatically resubmit timed-out uploads.

## Reference(s):

- [Server-resolved source release](https://github.com/leo-cheung-itlger/rmbase-agent-skill/tree/main/skills/rmbase)
- [RMBase project](http://bioinformaticsscience.cn/rmbase/)
- [RMBase database publication (PMID 37956310)](https://pubmed.ncbi.nlm.nih.gov/37956310/)
- [Capability audit](artifact/references/endpoints.md)
- [Output and cache contracts](artifact/references/schemas.md)

## Skill Output:

**Output Type(s):** [Scientific data, Guidance, Files]

**Output Format:** [JSON query results or TSV with a JSON provenance sidecar; agent summaries in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include species, assembly, retrieval provenance, pagination status, and warnings where applicable.]

## Skill Version(s):

0.1.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
