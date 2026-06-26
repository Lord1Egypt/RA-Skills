## Description: <br>
Use for RAGFlow dataset tasks: create, list, inspect, update, or delete datasets; upload, list, update, or delete documents; start or stop parsing; check parse status; retrieve chunks with search.py; and list configured models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redredrrred](https://clawhub.ai/user/redredrrred) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage RAGFlow datasets and documents, run or stop parsing, inspect parse status, retrieve chunks, and list configured models through bundled Python commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload files and retrieve document chunks from a configured RAGFlow server. <br>
Mitigation: Use it only with trusted RAGFlow endpoints and avoid uploading confidential or regulated files unless authorized. <br>
Risk: Dataset and document update, delete, parse, and stop operations can affect existing RAGFlow content. <br>
Mitigation: Use a least-privileged API key and confirm exact dataset or document IDs before executing state-changing commands. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/redredrrred/rrragflow-skill) <br>
- [Output Format Reference](reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses python3 scripts with RAGFLOW_API_URL and RAGFLOW_API_KEY environment variables.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
