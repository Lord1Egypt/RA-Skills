## Description:

Yixiaoer Rotator Skill helps agents sync Yixiaoer platform accounts, persist per-platform rotation state, and select the next account for multi-platform publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lsx1205](https://clawhub.ai/user/lsx1205)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and publishing workflow operators use this skill to rotate among authorized Yixiaoer accounts across platforms without repeatedly selecting the same account. Agents can use it to run sync, status, reset, and next-account commands as part of an automated publishing flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes a separately installed dependency while API credentials and the full process environment are available.

Mitigation: Install only when both packages are trusted, review or pin the dependency where possible, and run it from a limited shell environment without unrelated secrets.

Risk: The local state file stores account rotation metadata that may remain after account access changes.

Mitigation: Treat the state file as account metadata and manually clean it up or resync after permissions or account ownership changes.

## Reference(s):

- [Yixiaoer Rotator Configuration](references/config.md)
- [Yixiaoer Skill Dependency](https://clawhub.ai/yixiaoer-skill)
- [Yixiaoer Website](https://www.yixiaoer.cn)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output with a local JSON state file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires YIXIAOER_API_KEY, YIXIAOER_MEMBER_ID, and the separately installed yixiaoer-skill dependency.]

## Skill Version(s):

1.0.5 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
