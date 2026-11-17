## Description:

Fetches recent popular news by category, including technology, finance, sports, entertainment, automotive, domestic, international, military, and internet news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaker-coder](https://clawhub.ai/user/zaker-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve focused category news and trend updates when a prompt names or implies an industry or news domain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts an external ZAKER news API to fetch category news.

Mitigation: Deploy only where this disclosed API contact is acceptable, and make users aware that category requests rely on the external service.

Risk: Ambiguous prompts may map to the wrong news category.

Mitigation: Clarify uncertain category intent before fetching results.

Risk: The sample Python request does not set a timeout.

Mitigation: Add request timeouts before adapting the sample script for production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zaker-coder/skills/zaker-category-news)
- [ZAKER category article API](https://skills.myzaker.com/api/v1/article/category?v=1.0.6)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Code]

**Output Format:** [Markdown news list with linked titles, summaries, authors, and optional JSON from the category API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 20 category articles from the disclosed unauthenticated ZAKER API endpoint.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
