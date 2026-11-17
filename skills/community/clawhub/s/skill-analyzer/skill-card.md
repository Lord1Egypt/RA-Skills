## Description:

Quality scanner for OpenClaw skills. Evaluates functionality, security, usability, documentation, and best practices with weighted scoring. Use when: (1) Analyzing skill quality before publishing, (2) Finding improvement opportunities, (3) Security review of third-party skills. Pure Python - no dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeblackhole1024](https://clawhub.ai/user/codeblackhole1024)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to assess OpenClaw skill quality before publishing, compare skills, and identify improvement opportunities across functionality, security, usability, documentation, and maintainability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security-review function is materially unreliable and may give users misplaced confidence in unsafe third-party skills.

Mitigation: Treat results as a lightweight quality checklist only, and perform a separate manual security review before relying on a skill in production.

Risk: A LOW risk result can miss risks in nested scripts, non-Python files, network access, subprocess use, persistence, or sensitive data handling.

Mitigation: Manually inspect any reported LOW risk result and supplement the analyzer with appropriate static analysis, dependency review, and operational security checks.

## Reference(s):

- [Skill Analysis Scoring Rubric](references/scoring_rubric.md)
- [ClawHub Skill Analyzer Page](https://clawhub.ai/codeblackhole1024/skills/skill-analyzer)
- [Publisher Profile](https://clawhub.ai/user/codeblackhole1024)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain-text analysis report with optional JSON report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports weighted dimension scores, strengths, issues, and a risk level for a supplied skill directory.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
