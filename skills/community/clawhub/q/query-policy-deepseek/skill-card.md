## Description:

This skill helps agents batch query programming and technology specialty student admission policies by region in China using the DeepSeek API and produce CSV-ready policy rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zfm-mid](https://clawhub.ai/user/zfm-mid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers or education-policy analysts use this skill to run a DeepSeek-powered batch query over a line-delimited region list and generate Excel-compatible CSV rows for technology specialty student admission policies. Generated policy rows should be checked against official sources before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script exposes a hard-coded DeepSeek API credential.

Mitigation: Revoke or replace the bundled key before use, and configure the skill to read a user-provided credential from the environment or another approved secret store.

Risk: The script overwrites the configured output CSV at the start of each run.

Mitigation: Confirm the output path before execution and back up any existing CSV that must be retained.

Risk: Generated policy rows may be incomplete or inaccurate.

Mitigation: Treat generated rows as unverified and check admissions details against official school or government policy sources before relying on them.

## Reference(s):

- [Policy Guide](artifact/references/policy_guide.md)
- [DeepSeek Chat Completions API](https://api.deepseek.com/chat/completions)
- [ClawHub Skill Page](https://clawhub.ai/zfm-mid/skills/query-policy-deepseek)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, CSV files, guidance]

**Output Format:** [Markdown guidance with inline shell commands; the bundled script writes UTF-8-sig CSV output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script reads configured local input and progress files, calls the DeepSeek API once per region, and overwrites the output CSV at the start of each run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
