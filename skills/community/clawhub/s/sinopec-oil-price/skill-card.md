## Description:

Sinopec Oil Price lets agents query real-time Sinopec gasoline and diesel prices by Chinese province and report price changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[15878033657](https://clawhub.ai/user/15878033657)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check Sinopec oil prices for supported Chinese provinces and compose price-change summaries for monitoring workflows.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Dependency hardening issues may affect install integrity or vulnerability posture.

Mitigation: Regenerate the lockfile from a trusted registry and update vulnerable dependencies before installing or deploying.

Risk: Monitoring mode can create local history files and cron examples can make the skill run repeatedly.

Mitigation: Enable monitoring or cron only when recurring execution and local history storage are intended, and review the write location and permissions.

Risk: Returned oil prices are informational and may vary at actual gas stations.

Mitigation: Use the output as reference data and verify prices at the station or official channel before relying on them for transactions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/15878033657/skills/sinopec-oil-price)
- [API Reference](references/api.md)
- [Usage Examples](references/examples.md)
- [Sinopec Mobile Oil Price Endpoint](https://cx.sinopecsales.com/yjkqiantai)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON data objects and plain-text price summaries; documentation may include Markdown examples and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network calls query Sinopec's endpoint; monitoring can write local history JSON files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
