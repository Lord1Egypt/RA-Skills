## Description: <br>
Use for RAGFlow dataset tasks: create, list, inspect, update, or delete datasets; upload, list, update, or delete documents; start or stop parsing; check parse status; retrieve chunks with search.py; and list configured models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yingfeng](https://clawhub.ai/user/yingfeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage RAGFlow datasets, documents, parsing jobs, retrieval queries, and configured models through bundled command-line helpers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses RAGFLOW_API_KEY to manage RAGFlow resources. <br>
Mitigation: Use the least-privileged RAGFlow credential available and rotate it if exposure is suspected. <br>
Risk: Dataset or document deletion can remove RAGFlow content when exact IDs are supplied. <br>
Mitigation: List the target items first, verify exact dataset or document IDs, and require explicit confirmation before deletion. <br>
Risk: Document uploads send local files to the configured RAGFlow service. <br>
Mitigation: Verify RAGFLOW_API_URL and upload only files that are intended for that RAGFlow instance. <br>


## Reference(s): <br>
- [RAGFlow skill page](https://clawhub.ai/yingfeng/ragflow-skill) <br>
- [Output Format Reference](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses RAGFLOW_API_URL and RAGFLOW_API_KEY; command output should preserve returned API fields exactly.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
