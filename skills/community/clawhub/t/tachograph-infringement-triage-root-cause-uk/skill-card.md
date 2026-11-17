## Description:

Triages tachograph infringements, identifies common patterns, and outputs "what to check next" prompts and weekly review notes for UK tacho/WTD reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kowl64](https://clawhub.ai/user/kowl64)

### License/Terms of Use:


## Use Case:

Transport managers and compliance reviewers use this skill to turn weekly UK tachograph and WTD infringement records into manager-facing review notes, per-driver triage actions, root-cause prompts, and next checks.

### Deployment Geography for Use:

United Kingdom

## Known Risks and Mitigations:

Risk: Triage notes could be mistaken for final compliance, investigation, or disciplinary decisions.

Mitigation: Treat outputs as prompts for manager review and verify every proposed follow-up against source records and the organization's policy.

Risk: Incomplete downloads, missing days, or unclear record extracts could lead to unsupported conclusions.

Mitigation: Flag incomplete records as data gaps and ask for missing driver, period, source, or RAG history before escalation-dependent conclusions.

Risk: Root-cause suggestions could imply blame before operational context is checked.

Mitigation: Keep language neutral and frame root causes as questions or checks covering route plans, delays, training, device issues, and process gaps.

## Reference(s):

- [Common infringement patterns](artifact/references/common-infringement-patterns.md)
- [What to check next playbook](artifact/assets/what-to-check-next-playbook.md)
- [Weekly Tacho & WTD Compliance Review Pack](artifact/assets/weekly-review-pack-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown files with manager-facing summaries, per-driver triage actions, root-cause prompts, and follow-up guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires driver list, date range, and infringement summaries; asks for missing period, driver list, or RAG history before escalation-dependent conclusions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
