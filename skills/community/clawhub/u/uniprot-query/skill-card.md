## Description: <br>
Query UniProt for protein sequences, accession lookups, metadata, and criteria-based protein searches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollyya](https://clawhub.ai/user/hollyya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to look up UniProt accessions, search proteins by gene, organism, function, or disease, and retrieve structured protein metadata, sequences, annotations, and text reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Protein queries and returned metadata are sent to and retrieved from the UniProt REST API. <br>
Mitigation: Avoid sensitive research terms in queries when external API access is a concern. <br>
Risk: Example workflows can store returned UniProt metadata and reports locally. <br>
Mitigation: Use a non-sensitive output directory and remove saved reports when no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hollyya/uniprot-query) <br>
- [UniProt API documentation](https://www.uniprot.org/api-documentation) <br>
- [UniProt query fields reference](references/query_fields.md) <br>
- [UniProt metadata fields reference](references/metadata_fields.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, JSON structures, and text report examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Example scripts may generate local JSON metadata and text report files under ./tmp/uniprot.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
