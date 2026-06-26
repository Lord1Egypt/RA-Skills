## Description: <br>
Read-only access to Up Bank accounts, transactions, categories, and tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashleyjackson](https://clawhub.ai/user/ashleyjackson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent retrieve read-only Up Bank account, transaction, category, tag, attachment, webhook, and connectivity information after user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive Up Bank account and transaction information after user approval. <br>
Mitigation: Install it only when that access is acceptable, approve calls only for information requested, and avoid displaying unnecessary transaction details. <br>
Risk: A persistent or leaked UP_API_TOKEN could allow continued read access to financial data. <br>
Mitigation: Use a session-scoped token when possible, do not store it permanently, and revoke it when the skill is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ashleyjackson/upbank) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown or plain text summaries with API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only API access; requires UP_API_TOKEN and per-call user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
