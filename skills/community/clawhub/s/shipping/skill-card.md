## Description: <br>
Plan and manage parcel shipping decisions with carrier selection, landed-cost math, customs checks, and delivery exception playbooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External operations teams, sellers, and fulfillment staff use this skill to plan parcel shipments, compare carrier options by landed cost and SLA risk, prepare customs details, and respond to delivery exceptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory may retain customer, account, tracking, or business details under ~/shipping/. <br>
Mitigation: Use manual activation if broad engagement is not desired, and periodically review or redact ~/shipping/memory.md. <br>
Risk: The skill provides advisory shipping, customs, and exception-handling guidance without direct carrier account access or carrier API verification. <br>
Mitigation: Confirm rates, deadlines, restricted-item status, documentation, and claim deadlines in authoritative carrier or customs systems before purchasing labels or promising outcomes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/shipping) <br>
- [Shipping Operations homepage](https://clawic.com/skills/shipping) <br>
- [Setup](artifact/setup.md) <br>
- [Carrier Selection](artifact/carrier-selection.md) <br>
- [International Customs](artifact/international-customs.md) <br>
- [Exception Playbook](artifact/exception-playbook.md) <br>
- [Memory Template](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with checklists, tables, formulas, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not call carrier APIs or purchase labels by itself; may guide updates to local memory under ~/shipping/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
