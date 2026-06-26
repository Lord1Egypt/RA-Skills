## Description: <br>
Detects feature drift in tabular ML models using Superwise Compare Distribution policies, handles dataset setup and inference ingestion, and can send Telegram alerts when drift is detected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mark-stadtmueller](https://clawhub.ai/user/mark-stadtmueller) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML engineers use this skill to configure Superwise drift monitoring for tabular models, upload training and inference data, create categorical drift policies, and receive operational drift summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected training and inference records are sent to Superwise for drift monitoring. <br>
Mitigation: Use only approved datasets and least-privilege Superwise credentials, and confirm that the data is appropriate for the Superwise workspace before upload. <br>
Risk: Drift summaries may be sent to Telegram. <br>
Mitigation: Route alerts only to approved chats and avoid including sensitive feature values or model data in alert text. <br>
Risk: A deployed /run-check endpoint can trigger ingestion, policy polling, and alerts. <br>
Mitigation: Restrict access to the endpoint and protect deployment environment variables with a secret manager or platform-level secret storage. <br>
Risk: Unpinned dependencies can change behavior over time in production deployments. <br>
Mitigation: Pin and review Python dependencies before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mark-stadtmueller/superwise-drift-detection-skill) <br>
- [Superwise MCP documentation](https://docs.superwise.ai/mcp) <br>
- [Superwise Python SDK MCP reference](https://mcp.sdk.docs.superwise.ai/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, text] <br>
**Output Format:** [Markdown guidance with shell commands, environment configuration, Python code paths, and JSON-style drift summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Superwise APIs, a configured inference endpoint, and Telegram when executed by the user.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release metadata and skill.py metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
