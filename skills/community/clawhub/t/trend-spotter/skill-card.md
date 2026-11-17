## Description:

Trend Spotter helps campaign teams identify social and cultural trends, score brand fit, map timing, and decide whether to participate, watch, or skip.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing teams, creators, and campaign strategists use this skill to identify timely trends for a brand or industry, evaluate brand fit and safety, and produce campaign timing recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may apply the workflow to general campaign-timing or content-theme requests.

Mitigation: Confirm the user wants trend analysis and capture brand, platform, audience, geography, and time horizon before producing recommendations.

Risk: The skill can save trend reports and durable trend notes to local memory.

Mitigation: Review memory writes for sensitive campaign, audience, or brand strategy details before retaining or sharing them.

Risk: Single-source trend signals can be misleading or stale.

Mitigation: Label single-source findings as Estimated and prefer corroboration from two independent sources before making act-now recommendations.

## Reference(s):

- [Trend Spotter Templates](references/templates.md)
- [Keyless Multi-Source Trend Scout](references/trend-scout-recipe.md)
- [Repository Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/skills/trend-spotter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown trend report with tables, ranked recommendations, go/caution/skip calls, and optional shell command snippets for keyless trend scouting.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save markdown reports under memory/influencer/trend-spotter/ and durable notes to memory/hot-cache.md when memory is available.]

## Skill Version(s):

19.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
