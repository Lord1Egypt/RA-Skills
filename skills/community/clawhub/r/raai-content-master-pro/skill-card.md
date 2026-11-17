## Description:

Full-cycle content marketing system for Russian-speaking businesses: strategy, production, funnel logic, email, analytics, and reporting without automatic publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raaipro](https://clawhub.ai/user/raaipro)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, business owners, content managers, and agencies use this skill to turn product, audience, channel, goal, and tone inputs into Russian-language content strategy, monthly plans, SEO topic clusters, posts, repurposed formats, email sequences, funnel plans, competitor analysis, headline tests, and content reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outputs may stay bound to RAAI-specific examples or rules instead of the user's configured business.

Mitigation: Before use, remove or rewrite RAAI-specific runtime rules and test generated content against the intended business profile.

Risk: The skill declares several high-value API, Telegram, Sheets, and email-marketing credentials even though server metadata says it does not make requests.

Mitigation: Do not provision these credentials unless a separate reviewed integration requires them, and scope any provided credentials to the minimum necessary permissions.

Risk: The installer references files that are not present in the artifact package.

Mitigation: Repair and re-test installation before deployment, or install manually from the reviewed files.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/raaipro/skills/raai-content-master-pro)
- [Quick start examples](examples/quick-start.md)
- [Anti-fail guidance](docs/anti-fail.md)
- [ROI notes](docs/roi.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and structured text templates for content strategy, plans, posts, email sequences, competitor analysis, headline tests, funnel planning, and reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided business, audience, channel, goal, tone, and length or format constraints before generating content.]

## Skill Version(s):

3.5.5 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
