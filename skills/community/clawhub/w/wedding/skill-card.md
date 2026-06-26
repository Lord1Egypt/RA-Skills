## Description: <br>
Wedding.skill is a wedding planning co-pilot that tracks budgets, vendors, guest lists, timelines, seating constraints, and couple decisions from user-provided planning details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realteamprinz](https://clawhub.ai/user/realteamprinz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users planning a wedding use this skill to organize budget, vendors, guest details, seating constraints, timelines, and day-of plans. It helps turn user-provided planning details into reminders, summaries, tradeoff guidance, and local planning records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store private wedding budget, vendor, guest, and family details locally. <br>
Mitigation: Install only if local storage under ~/.wedding-skill/ is acceptable, avoid payment credentials and unnecessary sensitive guest details, and delete that folder when the planning history is no longer needed. <br>
Risk: Drafted vendor messages, reminders, budget summaries, or planning suggestions may be incomplete or unsuitable for the couple's circumstances. <br>
Mitigation: Review messages, deadlines, contract details, and budget changes before sending or acting on them; consult qualified advisors for loans, credit, or financial planning. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/realteamprinz/wedding) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown guidance and locally stored Markdown/JSONL planning files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local files under ~/.wedding-skill/ when the agent maintains planning memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
