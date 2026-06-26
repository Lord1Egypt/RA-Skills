## Description: <br>
Helps verify publisher identity integrity in AI agent ecosystems by surfacing impersonation, key rotation anomalies, and gaps in the trust chain between skill publishers and their claimed identities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security reviewers, and marketplace operators use this skill to evaluate publisher identity signals before adopting or recommending agent skills. It helps prioritize investigation of possible impersonation, account takeover, key rotation anomalies, and weak cross-platform identity corroboration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publisher identity ratings can be mistaken for proof of malicious or trustworthy behavior. <br>
Mitigation: Treat SUSPICIOUS or UNVERIFIED ratings as investigation prompts, verify important claims independently, and avoid providing private account data or credentials unless a future version clearly justifies that access. <br>


## Reference(s): <br>
- [Publisher Identity Verifier on ClawHub](https://clawhub.ai/andyxinweiminicloud/publisher-identity-verifier) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown identity report with scores, timelines, risk ratings, and recommended actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include VERIFIED, PARTIAL, UNVERIFIED, or SUSPICIOUS trust ratings for investigated publishers.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
