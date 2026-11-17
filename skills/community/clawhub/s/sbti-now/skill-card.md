## Description:

Runs a self-contained SBTI personality test in English, Simplified Chinese, or Traditional Chinese using bundled questions, local scoring scripts, and a manual fallback workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fechin](https://clawhub.ai/user/fechin)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to take or rerun an entertainment-first SBTI personality test and receive a localized personality code, score, vector, nearby matches, and shareable summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake SBTI personality results for a clinical or professional assessment.

Mitigation: Present the test as entertainment-first and not clinical; avoid diagnostic, medical, employment, or other high-stakes claims.

Risk: The skill asks personal preference and relationship-style questions.

Mitigation: Keep responses local to the session and avoid requesting credentials or unnecessary identifying information.

## Reference(s):

- [Manual Workflow](references/manual-workflow.md)
- [SBTI Online Version](https://sbti.now/)
- [ClawHub Skill Page](https://clawhub.ai/fechin/skills/sbti-now)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown result summaries, with optional JSON output from the bundled local script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports English, Simplified Chinese, and Traditional Chinese; results include score, 15-dimension vector, top 3 matches, and shareable summary.]

## Skill Version(s):

1.0.0 (source: release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
