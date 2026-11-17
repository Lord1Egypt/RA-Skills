## Description:

Analyzes workplace images and videos to identify employee phone use and report usage frequency and duration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Employers and workplace administrators use the skill to review authorized workplace images or video for apparent phone use and receive counts, duration summaries, and management suggestions. It also supports retrieving prior analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates this skill suspicious with high confidence, citing unexpected account and credential handling, remote processing of workplace media without clear disclosure, and an export-only option that may still run analysis.

Mitigation: Before installation or use, verify where media and identity data are sent, obtain appropriate authorization for remote processing and account creation, and confirm whether export-only use performs analysis.

Risk: The security scan is partial because a referenced path was missing, so the available findings do not fully cover that reference.

Mitigation: Review the missing reference and repeat the security assessment when the complete referenced material is available.

## Reference(s):

- [API documentation](artifact/references/api_doc.md)
- [Skill introduction](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured analysis results with counts, duration summaries, warnings, recommendations, and report links; JSON or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include employee phone-use detections and historical report links.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
