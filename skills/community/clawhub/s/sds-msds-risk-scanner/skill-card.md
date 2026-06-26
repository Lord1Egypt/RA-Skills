## Description: <br>
Extract hazard codes and safety info from chemical safety datasheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, lab safety reviewers, and compliance teams use this skill to extract GHS H-codes, P-codes, safety summaries, and PPE recommendations from SDS/MSDS content for reviewable safety documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted hazard codes or safety summaries may be incomplete or incorrect for a given SDS/MSDS. <br>
Mitigation: Treat outputs as draft safety summaries and verify extracted codes, PPE recommendations, and risk levels against the original SDS/MSDS before using them. <br>
Risk: The skill is not sufficient as the sole basis for compliance, emergency response, or PPE decisions. <br>
Mitigation: Use qualified human review and applicable safety procedures before relying on outputs for regulated or emergency contexts. <br>


## Reference(s): <br>
- [Audit Reference](references/audit-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/sds-msds-risk-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with structured safety findings and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include extracted H-codes, P-codes, risk level, safety summary, PPE recommendations, assumptions, validation needs, and unresolved items.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
