## Description: <br>
Tax is a local-first tax recordkeeping skill that captures tax documents, receipts, expenses, notices, missing-item reminders, and CPA-ready handoff summaries without providing tax advice or final calculations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agenticio](https://clawhub.ai/user/agenticio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals, freelancers, and small businesses use this skill to preserve tax-relevant facts throughout the year, track expected or missing records, and prepare organized Markdown and CSV materials for CPA, EA, accountant, or tax software review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive tax records may remain in local persistent storage longer than intended. <br>
Mitigation: Use the skill only in a trusted private workspace, archive completed years, and remove records that no longer need to be retained. <br>
Risk: Generated handoff summaries may include incomplete facts or unresolved tax treatment questions. <br>
Mitigation: Review summaries before sharing and confirm tax treatment, filing positions, and calculations with a licensed professional. <br>
Risk: Users may ask for legal or tax judgments that the skill is not designed to provide. <br>
Mitigation: Record the underlying fact, flag the issue for professional review, and avoid final advice, filing positions, or tax liability calculations. <br>


## Reference(s): <br>
- [ClawHub Tax skill page](https://clawhub.ai/agenticio/tax) <br>
- [CPA Handoff](references/cpa-handoff.md) <br>
- [Cross-Year Memory](references/cross-year-memory.md) <br>
- [Facts vs. Judgments](references/fact-vs-judgment.md) <br>
- [Recordkeeping](references/recordkeeping.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, CSV, JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown and CSV summaries, JSON local records, concise text guidance, and Python script commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores tax memory locally under ~/.openclaw/workspace/memory/tax/ and preserves raw user wording for later review.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
