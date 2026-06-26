## Description: <br>
YC Resource Import parses tourism resource contracts from local or cloud files, extracts hotel, transport, attraction, activity, SPA, club, restaurant, and afternoon-tea records into fixed-schema CSV rows, and can append them to production data stores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[errsr](https://clawhub.ai/user/errsr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel operations teams and developers use this skill to convert Bali tourism supplier contracts and resource files into standardized CSV records for catalog or database ingestion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change production CSV or database data, archive or delete files, and perform online enrichment without clearly bounded user control. <br>
Mitigation: Review before installing, start with approved contract folders and non-production test CSVs, require an explicit dry run, and require confirmation before production append, archive, or delete steps. <br>
Risk: Online enrichment may send contract-derived data outside the local environment. <br>
Mitigation: Make network enrichment opt-in and clearly state what contract-derived data may be sent externally before execution. <br>


## Reference(s): <br>
- [YC Resource Import on ClawHub](https://clawhub.ai/errsr/yc-resource-import) <br>
- [Global Tourism Resource Feature Tags Quick Reference V4.0](artifact/references/8类特色标签快速查阅表.md) <br>
- [Bali Zone ID Mapping Table V4.0](artifact/references/Zone映射表.md) <br>
- [Bali Tourism Resource Standardization Documentation](artifact/references/巴厘岛旅游资源标准化文档体系.md) <br>
- [Evaluation Cases](artifact/evals/评测用例.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CSV files, status text, installation commands, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces fixed-schema tourism-resource records and may append rows to existing CSV or database-backed production data.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
