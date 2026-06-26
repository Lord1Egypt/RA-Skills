## Description: <br>
Performs end-to-end SEO audit and on-page optimization by analyzing live SERP, competitor content, backlink data, and generating actionable rewrite guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h4gen](https://clawhub.ai/user/h4gen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External site owners, SEO practitioners, and developers use this skill to diagnose why a page is not ranking for a target keyword and generate intent-aligned rewrite guidance, backlink opportunities, and ordered next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup guidance includes an update-all command that can change installed ClawHub skills beyond this SEO workflow. <br>
Mitigation: Install only the four named dependencies and run a global skill update only when that broader change is intentional. <br>
Risk: The metadata lists several model-provider API keys even though the workflow needs only one supported summarization provider. <br>
Mitigation: Provide only the single model-provider key planned for use and rely on the skill's MissingAPIKeys and Partial output sections when a stage is blocked. <br>
Risk: SEO enrichment depends on Maton and connected search or SEO accounts, which may expose account-level data depending on granted scopes. <br>
Mitigation: Review Maton and OAuth scopes before connecting search-console or SEO accounts, and use fallback on-page analysis when provider access is unavailable. <br>


## Reference(s): <br>
- [SEO Ranker on ClawHub](https://clawhub.ai/h4gen/seo-ranker) <br>
- [Inspected upstream skills](references/inspected-skills.md) <br>
- [Semrush official trial entry page](https://www.semrush.com/sem/) <br>
- [Ahrefs Webmaster Tools](https://ahrefs.com/webmaster-tools) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured sections and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Partial, MissingAPIKeys, DataGateStatus, SERPFindings, OptimizedMarkdown, BacklinkOpportunities, and NextActions sections depending on available credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
