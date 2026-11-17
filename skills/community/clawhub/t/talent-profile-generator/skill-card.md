## Description:

Generates enterprise talent profiles, competency portraits, hiring criteria, interview focus areas, and candidate personas for specified roles using provided role context and public job-posting benchmarks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linuoxu](https://clawhub.ai/user/linuoxu)

### License/Terms of Use:

MIT-0

## Use Case:

HR, recruiting, and talent-management users use this skill to turn a role, level, culture, and business context into a structured talent portrait for JD optimization, interview design, candidate evaluation, and workforce review. It is especially oriented to Chinese-language enterprise hiring workflows and public job-posting benchmarks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Talent profiles can become misleading if generated from incomplete role, level, culture, or benchmark inputs.

Mitigation: Treat incomplete outputs as drafts, review the listed missing information, and validate assumptions with current role owners or representative job samples.

Risk: Hiring criteria may introduce inappropriate or discriminatory screening factors if users add non-job-related attributes.

Mitigation: Keep criteria tied to observable job behaviors and avoid protected or non-essential attributes such as gender, age, marital status, ethnicity, religion, household registration, or disability.

Risk: Public job-posting benchmarks may be unavailable, stale, or too limited for a specific market segment.

Mitigation: Disclose benchmark limits, avoid fabricating sources, and request user-provided JD samples when live recruitment-platform access is unavailable.

## Reference(s):

- [Talent profile output template](references/output-template.md)
- [ClawHub skill page](https://clawhub.ai/linuoxu/skills/talent-profile-generator)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with tables and optional Mermaid diagram]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese output and asks for confirmation when role, level, culture, or benchmark inputs are incomplete.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
