## Description: <br>
Use for RAGFlow dataset and retrieval tasks: create, list, inspect, update, or delete datasets; list, upload, update, or delete documents in a dataset; start or stop parsing uploaded documents; check parser status through `parse_status.py`; and retrieve relevant chunks from RAGFlow datasets with `search.py`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Magicbook1108](https://clawhub.ai/user/Magicbook1108) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage RAGFlow datasets and documents, trigger or stop parsing, inspect model availability, and retrieve relevant chunks from configured datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send document contents, filenames, queries, and a bearer API key to the configured RAGFlow server. <br>
Mitigation: Use only a trusted RAGFlow server in RAGFLOW_API_URL and protect RAGFLOW_API_KEY as a credential. <br>
Risk: Dataset and document deletion can remove content from RAGFlow. <br>
Mitigation: Limit deletion to exact dataset or document IDs and require explicit user confirmation before running delete commands. <br>
Risk: Broad progress checks in shared environments can expose status from multiple datasets. <br>
Mitigation: Prefer dataset-specific progress checks when operating in shared environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Magicbook1108/test-ragflow) <br>
- [Output Format Reference](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, lists, JSON code blocks, quoted retrieved chunks, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JSON script output when available and preserves API error fields for user-facing reporting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
