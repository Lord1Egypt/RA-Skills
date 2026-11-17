## Description:

紫微斗数双人合盘：先以 zwds-cli 各排一盘，再将两份 data 送入 hepan-cli 得 0-100 匹配分、维度分项与 hits。

This skill is ready for commercial/non-commercial use.

## Publisher:

[luyao-inc](https://clawhub.ai/user/luyao-inc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to compute structured Zi Wei Dou Shu compatibility for two charts, including an overall score, dimension-level scoring, and evidence hits for later interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user-controlled rule version can make the skill read unintended local JSON files.

Mitigation: Install only when the caller path to the CLI is trusted, or patch rule_version handling to allowlist known versions such as compat/v1 and reject traversal segments.

Risk: Error messages may disclose local paths and stdin parsing lacks an explicit input-size limit.

Mitigation: Avoid exposing raw CLI errors to untrusted users and enforce an input-size limit before parsing stdin.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luyao-inc/skills/zwds-hepan-openclaw)
- [zwds-hepan reference](reference.md)
- [Sample compatibility payload](examples/sample-compat-payload.json)
- [Compatibility rule pack v1](hepan-cli/src/rules/compat/v1.json)
- [Star grouping table](hepan-cli/src/tables/star_groupings.json)
- [Star pair score table](hepan-cli/src/tables/star_pair_scores.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying CLI returns one JSON object on success with score, confidence, rule_version, dimensions, hits, and penalty_total.]

## Skill Version(s):

1.0.0 (source: server release metadata and hepan-cli/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
