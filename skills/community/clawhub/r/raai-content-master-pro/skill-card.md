## Description: <br>
Full-cycle content marketing system for Russian-speaking businesses covering strategy, content production, funnel logic, email, and analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raaipro](https://clawhub.ai/user/raaipro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers, business owners, content managers, and agencies use this skill to plan and draft Russian-language content systems across Telegram, Instagram, email, SEO, funnels, competitor analysis, and reporting. It supports content strategy and drafting, but the artifact states that it does not automatically publish content or take over approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release requests sensitive API credentials for Telegram, Google Sheets, GetResponse, Unisender, Anthropic, and OpenAI even though the active instructions do not clearly require every credential. <br>
Mitigation: Provide only credentials that are necessary for a verified workflow, use scoped or disposable credentials where possible, and avoid storing production secrets in shared configuration files. <br>
Risk: Generated marketing claims, testimonials, customer metrics, competitor comparisons, or regulated-topic content may be inaccurate or unsuitable for publication. <br>
Mitigation: Review and approve all generated content before publishing, validate claims against source data, and remove unsupported customer or competitor statements. <br>
Risk: The skill depends on accurate business, audience, channel, tone, and analytics inputs; weak or fabricated inputs can produce weak guidance. <br>
Mitigation: Fill configuration with current business facts, channel data, and constraints before use, and treat generated plans as drafts for human editing. <br>


## Reference(s): <br>
- [Content Master Pro on ClawHub](https://clawhub.ai/raaipro/raai-content-master-pro) <br>
- [RAAIPRO publisher profile](https://clawhub.ai/user/raaipro) <br>
- [Quick start examples](artifact/examples/quick-start.md) <br>
- [Onboarding guide](artifact/docs/onboarding.md) <br>
- [Anti-fail guidance](artifact/docs/anti-fail.md) <br>
- [ROI notes](artifact/docs/roi.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured tables, checklists, templates, and concise prose] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference user-provided business, channel, audience, tone, and analytics inputs from configuration.] <br>

## Skill Version(s): <br>
3.5.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
