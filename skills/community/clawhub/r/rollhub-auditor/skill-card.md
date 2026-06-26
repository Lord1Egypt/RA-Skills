## Description: <br>
Audits Agent Casino fairness by verifying provably fair gambling results with SHA3-384 and AES-256-CTR checks, statistical randomness tests, RTP analysis, and report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rollhub-dev](https://clawhub.ai/user/rollhub-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External auditors, security reviewers, and developers use this skill to verify Agent Casino bets, run statistical fairness checks, calculate RTP, and generate audit reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live bets with a user API key and may spend funds. <br>
Mitigation: Use only a sandbox or tightly limited test account, and require explicit approval before running betting commands. <br>
Risk: The skill sends an API key to agent.rollhub.com. <br>
Mitigation: Confirm the endpoint and account scope before use, and avoid using credentials that grant broader access than the audit requires. <br>
Risk: The artifact includes an exposed ClawHub publishing token. <br>
Mitigation: The publisher should remove the token from release artifacts and rotate it before users install or run the skill. <br>
Risk: The audit script stores local betting records. <br>
Mitigation: Run in a controlled workspace and handle generated audit_data files as potentially sensitive account activity records. <br>


## Reference(s): <br>
- [Cryptographic Verification](references/crypto-verification.md) <br>
- [Statistical Tests for Fairness Auditing](references/statistical-tests.md) <br>
- [Agent Casino API](https://agent.rollhub.com/api/v1) <br>
- [ClawHub Skill Page](https://clawhub.ai/rollhub-dev/rollhub-auditor) <br>
- [Publisher Profile](https://clawhub.ai/user/rollhub-dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python and JavaScript verification snippets, and generated audit report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local audit_data JSONL and report files when the bundled audit script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
