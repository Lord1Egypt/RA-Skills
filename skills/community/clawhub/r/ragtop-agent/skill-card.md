## Description: <br>
Ragtop Agent helps an AI manage RAGTOP knowledge bases and perform agentic RAG retrieval, deep analysis, and cited summaries through RAGTOP API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qbs784](https://clawhub.ai/user/qbs784) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and knowledge workers use this skill to inspect RAGTOP knowledge bases, narrow retrieval to relevant documents, and synthesize cited answers from retrieved chunks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill defaults to an unencrypted private API URL if RAGTOP_API_URL is not set, which could send tokens and queries to an unintended internal host. <br>
Mitigation: Set RAGTOP_API_URL explicitly to the approved trusted endpoint, preferably HTTPS, before using the skill. <br>
Risk: The skill sends user queries and retrieved context to the configured RAGTOP backend. <br>
Mitigation: Use a scoped RAGTOP_API_TOKEN and avoid sending secrets, regulated data, or broad internal corpora unless the backend is approved for that data. <br>


## Reference(s): <br>
- [Agentic RAG Workflow Guidelines](references/workflow.md) <br>
- [ClawHub release page](https://clawhub.ai/qbs784/ragtop-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with curl command blocks, readable lists or tables, and cited synthesis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses RAGTOP_API_TOKEN and an optional RAGTOP_API_URL to call list and retrieval endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
