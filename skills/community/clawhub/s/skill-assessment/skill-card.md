## Description:

Agent skill quality checker. Input a skill directory or skill files; output trigger clarity, metadata issues, examples, safety boundaries, installability, portability risks, and prioritized fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to inspect skill directories for documentation completeness, code quality, configuration friendliness, maintenance signals, and prioritized fixes before publishing, installing, or comparing skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Assessment output can present fixed favorable scores or summaries even when checker results do not support them.

Mitigation: Treat scores and pass/fail summaries as advisory; inspect generated findings and raw checker outputs before using results for security, quality, or release decisions.

Risk: Installation changes local file permissions and may create a symlink under ~/.openclaw/skills.

Mitigation: Review install.sh before running it, run it from the intended skill directory, and avoid elevated privileges unless explicitly needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/skill-assessment)
- [Example assessment report](examples/sample_report.md)
- [Example configuration](examples/config.example.yaml)
- [Project homepage listed in artifact metadata](https://github.com/harrylabs0913/skill-assessment)
- [Project repository listed in artifact metadata](https://github.com/harrylabs0913/skill-assessment.git)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, or text assessment reports with console summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may be saved under reports/; assessment weights, thresholds, and checks are configurable.]

## Skill Version(s):

1.1.0 (source: evidence release metadata and artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
