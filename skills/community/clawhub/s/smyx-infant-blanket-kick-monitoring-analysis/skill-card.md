## Description:

Identifies babies kicking off blankets or exposing their bodies during sleep and alerts parents to cover them up to prevent catching a cold. | 婴儿蹬被监测技能，识别婴儿夜间睡觉踢开被子、身体裸露，及时提醒家长给宝宝盖被保暖，预防着凉感冒

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and caregivers use this skill to analyze infant sleep monitoring images or videos for blanket-kicking and body exposure, then receive structured results, reminders, recommendations, and report links. It can also query cloud-hosted historical monitoring reports associated with the internally resolved user identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive infant media and monitoring reports may be uploaded to cloud services.

Mitigation: Require publisher documentation for upload destinations, retention, access controls, and user consent before installation.

Risk: Active development HTTP configuration may expose data to insecure or unintended endpoints.

Mitigation: Require the publisher to remove or disable development HTTP endpoints and verify HTTPS production configuration before use.

Risk: Identity and reusable token handling may rely on plaintext local storage.

Mitigation: Move reusable tokens to secure secret storage, rotate existing tokens, and document identity handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-infant-blanket-kick-monitoring-analysis)
- [Skill demo](https://lifeemergence.com/sample.html)
- [API documentation](references/api_doc.md)
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON analysis reports with status text, recommendations, report links, and optional saved output files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports local file input, URL input, detailed output levels, saved report output, and cloud historical report listing.]

## Skill Version(s):

1.0.11 (source: server release evidence; artifact frontmatter reports 1.0.13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
