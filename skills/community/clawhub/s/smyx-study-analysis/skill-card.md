## Description:

Conducts video analysis of learning behavior for children and students, identifies poor learning habits, and provides structured reports and family education suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and caregivers use the skill to review a child's learning behavior video and receive structured observations about attention, posture, and study habits, along with family education suggestions. Reports are for educational reference and do not replace assessment by a teacher or mental health professional.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that local video may be sent for remote analysis without clear notice, and that analysis may continue despite an export-only request.

Mitigation: Before submitting a child's video, verify the service's video handling and export-only behavior, explain the remote analysis to the relevant people, and obtain appropriate consent.

Risk: The security evidence reports undeclared account and credential handling, possible credential transmission, and identity or credential data used in remote account requests.

Mitigation: Review account and credential data flows before use, and avoid providing sensitive identity or credential information until those flows are understood.

Risk: The security assessment is incomplete: Skillspector marked analysis partial because a local reference was missing, although AIG completed without findings.

Mitigation: Treat the suspicious verdict as unresolved and complete a security review before installing or sending sensitive content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-study-analysis)
- [API interface documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured analysis results in JSON or text, with Markdown report lists and education suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include attention and behavior observations, risk notices, suggestions, and report links; intended for family education reference.]

## Skill Version(s):

1.0.21 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
