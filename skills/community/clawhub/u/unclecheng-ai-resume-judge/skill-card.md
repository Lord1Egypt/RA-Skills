## Description:

Resume Score for the resume evaluates resume text or a local resume file against a 100-point AI resume rubric, detects non-AI industries, and returns cross-industry score analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unclecheng-li](https://clawhub.ai/user/unclecheng-li)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to score resumes, compare the result across seven rubric dimensions, and receive concise improvement guidance. It is intended for resume review workflows where the user understands that the scoring is rule-based and should be treated as advisory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume content can contain highly sensitive personal data.

Mitigation: Use only resumes the user explicitly provides for scoring and avoid submitting unnecessary personal details.

Risk: The CLI can save resume-derived output to a hard-coded local path.

Mitigation: Do not run the CLI until the output destination is made explicit and user-controlled.

Risk: Rule-based resume scores may be misleading if treated as objective hiring judgments.

Mitigation: Present scores as advisory resume feedback and require human review before employment-related decisions.

## Reference(s):

- [Scoring benchmark](references/scoring_benchmark.md)
- [ClawHub skill page](https://clawhub.ai/unclecheng-li/skills/unclecheng-ai-resume-judge)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown report with score tables, commentary, improvement suggestions, and optional JSON score data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include a timestamp, AI-field detection, raw score, dimensional scores, rating, and cross-industry equivalent score when applicable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
