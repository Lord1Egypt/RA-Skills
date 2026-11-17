## Description:

Evaluates Buddhist lectures, recitations, classes, and talks from audio or video by transcribing them, scoring content and delivery, checking doctrinal sources, and producing a charted HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gouchunlei2-png](https://clawhub.ai/user/gouchunlei2-png)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, and reviewers use this skill to assess Buddhist audio or video talks for doctrinal accuracy, structure, expression, audience fit, emotional impact, and independent contribution. It is intended for evaluation reports, not for pure transcript editing or general non-Buddhist speech scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency or model downloads may rely on mirrors or third-party package sources.

Mitigation: Install in an isolated environment, pin and verify dependencies or models where possible, and avoid third-party mirrors unless they are trusted.

Risk: Traditional Chinese inputs are converted to Simplified Chinese before processing and report generation.

Mitigation: Review source-sensitive passages against the original audio or transcript when exact traditional wording matters.

Risk: Scoring and source checks may be misleading if timestamped transcription is unavailable or inaccurate.

Mitigation: Use audio or video that supports timestamped transcription, and review cited source links and key scoring judgments before relying on the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gouchunlei2-png/skills/sikll)
- [Publisher profile](https://clawhub.ai/user/gouchunlei2-png)
- [Artifact README](artifact/README.md)
- [CBETA Online line reference example](https://cbetaonline.dila.edu.tw/zh/T46n1939_p0938c04)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Single-file HTML report with inline CSS.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires audio or video input. Audio analysis depends on timestamped transcription, and Traditional Chinese content is normalized to Simplified Chinese for processing and reports.]

## Skill Version(s):

2.26.0 (source: frontmatter, clawhub.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
