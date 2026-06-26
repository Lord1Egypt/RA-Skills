## Description: <br>
Use for RAGFlow dataset tasks: create, list, inspect, update, or delete datasets; upload, list, update, or delete documents; start or stop parsing; check parse status; retrieve chunks with `search.py`; and list configured models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liberalchang](https://clawhub.ai/user/liberalchang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage RAGFlow datasets and documents, run parsing workflows, retrieve chunks, and inspect configured models through bundled Python scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RAGFlow API key and sends requests to the configured RAGFlow server. <br>
Mitigation: Install only when the RAGFlow server is trusted, keep RAGFLOW_API_KEY protected, and verify RAGFLOW_API_URL before use. <br>
Risk: Upload commands send local files to the configured RAGFlow server. <br>
Mitigation: Upload only files intended for that server and confirm the target dataset before running upload scripts. <br>
Risk: Dataset and document delete operations perform API deletes once invoked. <br>
Mitigation: List exact targets first, confirm dataset or document IDs, and require explicit user confirmation before deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liberalchang/ragflow-skill-python) <br>
- [Output format reference](reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown responses with optional JSON code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses RAGFLOW_API_URL and RAGFLOW_API_KEY, prefers --json output, and preserves API error fields exactly.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
