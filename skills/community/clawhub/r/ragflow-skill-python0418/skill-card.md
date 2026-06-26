## Description: <br>
Use for RAGFlow dataset tasks: create, list, inspect, update, or delete datasets; upload, list, update, or delete documents; start or stop parsing; check parse status; retrieve chunks with search.py; and list configured models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liberalchang](https://clawhub.ai/user/liberalchang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage RAGFlow datasets, documents, parsing jobs, retrieval queries, and configured models through bundled Python scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The RAGFlow API key and uploaded files are sent to the configured RAGFLOW_API_URL. <br>
Mitigation: Install only when the configured RAGFlow endpoint is trusted and use the least-privileged RAGFlow key available. <br>
Risk: Dataset and document delete actions can remove RAGFlow resources. <br>
Mitigation: List exact target items first and require explicit user confirmation before executing delete commands. <br>
Risk: Uploads and update commands can send or modify user-selected dataset and document content. <br>
Mitigation: Confirm dataset IDs, document IDs, and file paths before running upload or update commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liberalchang/ragflow-skill-python0418) <br>
- [Output Format Reference](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with JSON code blocks and shell commands; bundled scripts can emit JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus RAGFLOW_API_URL and RAGFLOW_API_KEY; prefers exact API fields and JSON output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
