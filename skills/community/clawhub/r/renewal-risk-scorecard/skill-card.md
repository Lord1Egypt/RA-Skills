## Description: <br>
Use when a customer success manager, CS leader, or RevOps analyst needs to assess the renewal risk of a single SaaS account. Guides structured intake across five health dimensions, multi-signal Red/Yellow/Green scoring, and produces an overall risk tier, stakeholder map, save playbook, customer-facing talking points, and an internal escalation note. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer success managers, CS leaders, and RevOps analysts use this skill to assess one SaaS account's renewal risk, expose missing data, and produce a scorecard, stakeholder map, save playbook, talking points, and internal escalation note. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process confidential account data such as ARR, renewal dates, stakeholder names, support issues, and commercial terms. <br>
Mitigation: Use only account data authorized for the agent session, anonymize where practical, and follow organizational data handling rules. <br>
Risk: Incomplete or inaccurate account signals can produce misleading renewal risk scoring. <br>
Mitigation: Require supplied evidence for every dimension score, mark missing dimensions as Insufficient data, and review the final scorecard before relying on it. <br>
Risk: Generated talking points or escalation notes may expose sensitive internal context if shared without review. <br>
Mitigation: Review and edit customer-facing and leadership-facing text before distribution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/archlab-space/renewal-risk-scorecard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown scorecard with tables and concise prose] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-supplied account signals; no external data handling or tool execution is described.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
