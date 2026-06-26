## Description: <br>
Analyzes succulent images or videos to identify black rot, leaf melting, stretching, or healthy state, then returns severity, affected areas, confidence, and report links for history queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, greenhouse operators, flower shops, and developers use this skill to run succulent special-state detection on plant images or videos and to retrieve account-linked analysis history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads plant images or videos to a configured external service and links analyses to an open-id, username, or phone number. <br>
Mitigation: Use it only where this account-linked upload workflow is acceptable, and avoid submitting sensitive media or personal identifiers. <br>
Risk: Server security evidence flags token persistence, hardcoded/shared identifiers, and broad API helpers that are not tightly scoped to plant analysis. <br>
Mitigation: Review configuration before installation, remove or rotate shared credentials, and install only in environments where local token storage is acceptable. <br>
Risk: History retrieval can expose prior account-linked analysis records through the configured cloud service. <br>
Mitigation: Limit open-id sharing, verify the account context before listing reports, and avoid using shared accounts for private records. <br>


## Reference(s): <br>
- [API interface documentation](artifact/references/api_doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-succulent-special-state-detection-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown or JSON text returned from command-line/API workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a plant image or video, or a history-list query, plus an open-id for report storage and retrieval.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
