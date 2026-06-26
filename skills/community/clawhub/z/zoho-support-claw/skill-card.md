## Description: <br>
Integrates Zoho Desk with OpenClaw to ingest historical support tickets, store local embeddings, analyze open tickets, and propose draft replies using OpenAI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pretid](https://clawhub.ai/user/Pretid) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Support teams and developers use this skill to connect Zoho Desk ticket history with OpenAI-assisted analysis, helping generate draft replies for open support tickets from similar resolved cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Support-ticket content may contain sensitive customer or business data and is sent to OpenAI for embeddings and draft generation. <br>
Mitigation: Confirm organizational approval for external processing, redact secrets and regulated data before ingestion, and limit use to approved ticket categories. <br>
Risk: Historical ticket text and embeddings are stored locally in data/embeddings.json. <br>
Mitigation: Restrict file access, define retention and deletion controls, and avoid committing generated data files. <br>
Risk: The skill depends on Zoho and OpenAI credentials loaded from .env. <br>
Mitigation: Use least-privilege Zoho credentials, protect .env access, rotate exposed keys, and avoid logging or sharing credential values. <br>
Risk: The release is flagged as suspicious because sensitive support data handling lacks enough scoping, redaction, or retention guidance. <br>
Mitigation: Review before installing in a real support environment, pin or upgrade dependencies, test with a low ingest limit, and add operational controls before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Pretid/zoho-support-claw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON analysis results containing ticket IDs and draft replies, with CLI commands and environment configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft replies are generated from Zoho ticket details and locally stored embeddings of historical tickets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact manifest, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
