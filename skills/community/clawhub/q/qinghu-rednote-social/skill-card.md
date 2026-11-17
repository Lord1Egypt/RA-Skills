## Description:

This skill helps agents plan Xiaohongshu social-media campaigns with Qinghu API data for hot-topic research, note analysis, comment pain-point extraction, KOC/KOL screening, seeding plans, and Xiaohongshu seeding-code generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, social-media operators, agencies, and content strategists use this skill to research Xiaohongshu topics, deconstruct high-performing notes, identify audience pain points, screen KOC/KOL accounts, and draft seeding plans. Developers or agents may also use it to call Qinghu's API with user approval and produce concise strategy deliverables or exported datasets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Qinghu API key and can send Xiaohongshu query context to Qinghu's API.

Mitigation: Confirm user authorization before API calls, use only the provided key or approved environment variables, and avoid sending sensitive data.

Risk: Qinghu API calls may consume paid credits.

Mitigation: List the planned tools before first use, obtain explicit approval, and report actual Qinghu credit consumption from the response pointCost.

Risk: Larger Xiaohongshu result sets may be exported to local files.

Mitigation: Export only data the user is comfortable storing locally and keep chat previews concise.

Risk: Social-media analysis can be misleading when samples are small, stale, or mixed across sites or periods.

Mitigation: State the site, period, account scope, and sample size with conclusions, and avoid comparing incompatible datasets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-rednote-social)
- [Qinghu API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys)
- [Qinghu workflow authentication check](https://www.iqinghu.com/api/desktop/qh/workflow/page?pageNum=1&pageSize=5)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown responses with optional JSON request examples, shell/API call snippets, and exported table files for larger datasets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user approval before Qinghu API calls; larger record sets are exported instead of pasted into chat.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
