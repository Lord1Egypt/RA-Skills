## Description:

Analyze a website's topical relevance, content clusters, and pages that drift from its core purpose, then generate an interactive topic radius report with verified source excerpts or assess a draft's fit before publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[domainrankhq](https://clawhub.ai/user/domainrankhq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and content teams can use the skill to map the topics represented by a public website, review pages that may drift from its purpose, or check whether a draft fits the site before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow fetches public pages, and the optional standalone analyze command can send sampled page text and excerpts to OpenRouter.

Mitigation: Use public pages you are authorized to analyze, review excerpts before sharing reports, and use the local IDE workflow when you do not intend to send page text to OpenRouter.

Risk: The security scan rated the skill benign with medium confidence and reported partial component coverage.

Mitigation: Review the documented Node.js and optional API-key/network use before running, and keep OPENROUTER_API_KEY private.

## Reference(s):

- [Site Topic Relevance checker](https://domainrank.app/site-relevance)
- [Crawling methodology and limits](artifact/references/method.md)
- [Explicit OpenRouter CLI usage](artifact/references/openrouter.md)
- [ClawHub skill page](https://clawhub.ai/domainrankhq/skills/site-topic-relevance)

## Skill Output:

**Output Type(s):** [Analysis, HTML, JSON, Markdown]

**Output Format:** [Interactive HTML topic radius report with JSON and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include sampled page coverage, relevance scores, topic groupings, and source excerpts; crawl sampling is limited to 3–50 pages.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
