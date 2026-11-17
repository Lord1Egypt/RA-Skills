## Description:

Converts Chinese text reports into strict seller-report visualization component JSON for chart, card, timeline, alert, and influence layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Chinese-language report content into structured visualization modules. It is suited for report-to-dashboard drafting where output must follow the seller-report JSON component schema.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad visualization requests may select this skill even when the user does not want Chinese seller-report JSON.

Mitigation: Confirm that Chinese-language, seller-report formatted visualization JSON is the intended output before applying the skill to broad report-visualization prompts.

Risk: Generated chart configurations can be misleading if source reports lack sufficient raw data for the requested visualization type.

Mitigation: Review each generated component against the source report and avoid inferred, backfilled, or mixed-unit data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/report-to-visualization)
- [Anti-pattern reference](artifact/references/anti-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown fenced seller-report JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single modules array of visualization component configurations and is designed for Chinese-language reports.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
