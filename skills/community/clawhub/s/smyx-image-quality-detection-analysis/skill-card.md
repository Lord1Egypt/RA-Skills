## Description:

Detects camera image-quality issues such as black or white screens, color casts, stripes, noise, and blur for surveillance and camera self-check scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Security camera operators and developers can analyze camera images or video frames for common quality problems and review historical analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rates the skill suspicious because scanners report account and credential handling, broad network requests, and behavior that may not clearly fit its image-quality purpose; the scan is partial and evidence is incomplete.

Mitigation: Before installing, verify that its account and credential handling, network destinations, and media-upload behavior fit your environment. Avoid submitting sensitive footage until those details are clear.

## Reference(s):

- [API Reference](references/api_doc.md)
- [Skill Demo](https://lifeemergence.com/sample.html)
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-image-quality-detection-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [JSON analysis results and Markdown report lists with links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts image or video files and network URLs; documented formats are JPG, JPEG, PNG, MP4, AVI, and MOV, up to 10 MB. Results support equipment maintenance and do not replace professional hardware inspection.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
