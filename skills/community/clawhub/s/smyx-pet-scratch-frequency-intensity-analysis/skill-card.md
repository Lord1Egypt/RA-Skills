## Description:

Analyzes cat scratch-post videos for scratching frequency, session duration, and vibration-based intensity, and reports behavioral observations without diagnosing disease or prescribing behavior changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners and developers use the skill to review cat scratch-post videos and receive structured observations about scratching frequency, duration, estimated intensity, stress indicators, and claw health. The results are for behavioral reference and do not provide a diagnosis or behavior-correction advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends local videos or supplied video URLs to remote analysis services, and its workflow includes local account creation or reuse, cloud history retrieval, and report export links; the security review advises clarifying these behaviors before installation.

Mitigation: Use only videos you are authorized to share. Before installation, clarify account creation and storage, video transfer, history access, report export, and the behavior of export-only mode.

Risk: The security assessment is incomplete because a referenced local path was missing, so it does not establish that every referenced behavior was examined.

Mitigation: Review the missing reference and repeat the security review before relying on the skill.

## Reference(s):

- [API interface notes](references/api_doc.md)
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-pet-scratch-frequency-intensity-analysis)
- [Usage demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured JSON analysis results with Markdown summaries and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Intensity is estimated from observed vibration; camera angle and distance affect the relative estimate.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata; artifact frontmatter lists 1.0.23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
