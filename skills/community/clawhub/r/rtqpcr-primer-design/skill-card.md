## Description: <br>
Designs high-specificity RT-qPCR primers and probes with homology mapping, high-GC optimization, TaqMan/SYBR support, and off-target specificity checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zjuphD](https://clawhub.ai/user/zjuphD) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Molecular biology users and bioinformatics developers use this skill to design RT-qPCR primer/probe assay candidates for standard transcripts, predicted transcripts that need homology mapping, high-GC viral templates, and SYBR or TaqMan workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries NCBI for accessions provided by the user, which can disclose sensitive or unpublished sequence identifiers to that external service. <br>
Mitigation: Use only accessions whose NCBI lookup is acceptable for the project, and avoid submitting sensitive or unpublished identifiers unless that data flow has been approved. <br>
Risk: Primer and probe candidates may be unsuitable for a specific assay, sample type, or wet-lab condition even when they pass the automated checks. <br>
Mitigation: Review candidates against lab-specific assay criteria and validate experimentally before ordering primers or relying on assay results. <br>
Risk: The Python dependency list names requests without a pinned version. <br>
Mitigation: For controlled deployments, pin requests to a reviewed current version before installation. <br>


## Reference(s): <br>
- [RT-qPCR Primer Design Guidelines](references/guidelines.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zjuphD/rtqpcr-primer-design) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON-like primer/probe result data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query NCBI for accession sequence and annotation data supplied by the user.] <br>

## Skill Version(s): <br>
5.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
