## Description:

Helps project managers, program managers, and PMO analysts update RAID logs from reporting-period inputs and draft stakeholder status reports with delta-marked entries and RAG ratings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Project managers, program managers, and PMO analysts use this skill to turn meeting notes, blocker reports, decision memos, risk escalations, and dependency updates into an updated RAID log and a draft sponsor-facing status report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process confidential project, vendor, customer, or stakeholder information pasted by users.

Mitigation: Use sanitized summaries for HR-sensitive, legal, regulatory, or personal material, and keep sensitive detail outside stakeholder-facing output.

Risk: Draft RAG ratings and status language could be mistaken for published project status.

Mitigation: Keep the PM and sponsor review banner, treat all RAG ratings as proposals, and require sponsor accountability before publication.

Risk: Incorrect closure or manipulation of RAID entries could obscure the real project state.

Mitigation: Require explicit closure evidence, preserve delta labels, and record unsupported RAG disagreements for sponsor decision.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/archlab-space/skills/raid-log-update)
- [Open-Skill-Hub Feedback](https://github.com/archlab-space/Open-Skill-Hub/issues)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown draft containing an updated RAID log, delta summary, stakeholder status report, and open questions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-only output for PM and sponsor review; RAG ratings are proposed, not published status.]

## Skill Version(s):

0.1.1 (source: server release metadata and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
