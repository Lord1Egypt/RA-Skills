## Description:

Use this skill when a transportation engineer or planner wants to draft or review a Traffic Impact Analysis for a proposed development, covering agency scoping, ITE trip generation, HCM LOS, no-build/build scenarios, queues, turn-lane warrants, mitigation, and PE/PTOE stamp boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Transportation engineers, planners, site-development consultants, and land-use reviewers use this skill to draft Traffic Impact Analysis or Traffic Impact Study reports for proposed developments. The output is intended for licensed PE or PTOE review, verification, stamp, and submission.

### Deployment Geography for Use:

Global; defaults to U.S. agency practice unless the user names an international framework.

## Known Risks and Mitigations:

Risk: Draft report content could be mistaken for a stamped professional engineering deliverable.

Mitigation: Keep the output labeled as draft-only and require licensed PE or PTOE verification, stamp, and submission.

Risk: Incorrect or unsupported traffic counts, LOS results, queues, trip generation values, or agency assumptions could mislead a TIA review.

Mitigation: Use only user-supplied or agency-supplied data, mark software-derived results as coming from the PE's HCM run when absent, and require agency scoping confirmation.

Risk: Users outside the U.S. could apply U.S. TIA defaults where a different national or agency framework controls.

Mitigation: Ask users to name the applicable country, agency, or international framework before using non-U.S. assumptions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/archlab-space/skills/traffic-impact-analysis-report-drafter)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown draft reports, memos, tables, checklists, and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-only traffic impact analysis content requiring licensed PE or PTOE verification before submission.]

## Skill Version(s):

0.1.2 (source: server release evidence and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
