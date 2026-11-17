## Description:

Track manuscript resubmission deadlines and automatically generate phase-appropriate task breakdowns for academic researchers based on remaining time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Academic researchers use this skill to track manuscript resubmission deadlines, assess urgency from remaining time, and generate phase-appropriate revision task schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned or unnecessary package dependencies may create supply-chain review risk.

Mitigation: Review or remove requirements.txt dependencies before installation; avoid running pip install -r requirements.txt as written unless the dependencies are confirmed necessary and trusted.

Risk: Deadline calculations can be wrong if the default timezone does not match the user's actual submission context.

Mitigation: Specify the intended timezone explicitly and manually verify calculations for important submissions.

Risk: The delete command removes local deadline records without confirmation.

Mitigation: Review the target record before using delete and keep a backup of local deadline data when records are important.

## Reference(s):

- [Journal Deadlines Reference](references/journal_deadlines.md)
- [Revision Checklist](references/revision_checklist.md)
- [Task Templates](references/task_templates.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples and structured deadline summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, urgency assessment, task schedule, risks, caveats, and next checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
