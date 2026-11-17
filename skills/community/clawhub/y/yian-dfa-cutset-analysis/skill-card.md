## Description:

Updates DFA cut-set analysis worksheets in Excel workbooks by synchronizing Order 2 and 3 cut sets and marking additions and removals for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guiqulaihaiqing](https://clawhub.ai/user/guiqulaihaiqing)

### License/Terms of Use:

MIT-0

## Use Case:

Engineers use this skill to synchronize FTA minimal cut-set changes with the DFA Analysis-CutSet worksheet in an Excel workbook. It marks new and obsolete cut sets and drafts analysis fields for engineering review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: When a workbook contains multiple matching worksheets, the updater may use an outdated source worksheet while the built-in coverage check still reports success.

Mitigation: Work on a separate workbook copy, explicitly select the source and target worksheets, and independently verify the selected worksheets and requested orders.

Risk: Automatically drafted DFA entries may be inaccurate, especially entries classified under EPS ECU.

Mitigation: Have a safety engineer review every generated draft and preserve the review markers separately.

## Reference(s):

- [DFA cut-set analysis procedure](references/procedure.md)
- [ClawHub skill release](https://clawhub.ai/guiqulaihaiqing/skills/yian-dfa-cutset-analysis)

## Skill Output:

**Output Type(s):** [Files, Analysis, Guidance]

**Output Format:** [Updated Excel workbook (.xlsx) with synchronized cut-set rows, review markers, and draft DFA fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [New DFA field entries are drafts for engineering review.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
