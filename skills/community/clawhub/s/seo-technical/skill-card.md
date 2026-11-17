## Description:

Technical SEO audit across 9 categories: crawlability, indexability, security, URL structure, mobile, Core Web Vitals, structured data, JavaScript rendering, and IndexNow protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and SEO practitioners use this skill to audit technical SEO issues across crawlability, indexability, security, URL structure, mobile experience, Core Web Vitals, structured data, JavaScript rendering, and IndexNow support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill suggests optional SEO and Lighthouse commands that may depend on local tooling or package resolution.

Mitigation: Confirm the seogeo tooling and any SEO APIs are trusted before use, and prefer a pinned Lighthouse version or trusted preinstalled binary instead of npx lighthouse@latest.

Risk: Website audits may access or analyze sites outside the user's authority.

Mitigation: Run audits only for sites the user is authorized to test.

## Reference(s):

- [Agent-friendly pages audit reference](references/agent-friendly-pages.md)
- [Google AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/seo-technical)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with audit findings, priority sections, category scores, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference JSON output from SEO, Lighthouse, PageSpeed, CrUX, and site-rendering tools when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
