## Description: <br>
Answers tax-related questions using a configured private corporate tax knowledge base through RAGFlow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoxin139](https://clawhub.ai/user/zhaoxin139) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and tax operations teams can use this skill to route VAT, corporate income tax, personal income tax, tax benefits, and filing-process questions to a configured RAGFlow-backed enterprise knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends tax questions to the configured RAGFlow service, which may receive sensitive tax or business details. <br>
Mitigation: Use only a trusted RAGFlow server with privacy controls appropriate for the data being queried, and avoid submitting highly sensitive details unless that service is approved. <br>
Risk: The skill requires a RAGFlow API key and endpoint configuration. <br>
Mitigation: Provide a limited-scope API key, protect the environment file, and review the API URL carefully before use. <br>
Risk: Runtime dependencies are specified with minimum versions rather than pinned versions. <br>
Mitigation: Pin and review dependency versions in controlled or production deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaoxin139/taxragflow) <br>
- [Publisher profile](https://clawhub.ai/user/zhaoxin139) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text answers and error messages, with setup guidance in Markdown and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RAGFLOW_API_URL, RAGFLOW_API_KEY, and RAGFLOW_CHAT_ID to be configured before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
