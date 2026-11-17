## Description:

Access and summarize public financial news from Yicai, providing keyword-based headlines, industry statistics, and company event timelines without bulk scraping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to search, summarize, and monitor public Yicai financial news by keyword, channel, industry, or company event.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may browse live Yicai pages and summarize changing public news content.

Mitigation: Review generated summaries against source links and timestamps before using them for decisions.

Risk: Page automation or repeated access could exceed appropriate use of the source site.

Mitigation: Use light, rate-limited access only, avoid bulk collection, and follow the site's rules.

Risk: The skill is intended for public content and should not process private or sensitive data.

Mitigation: Provide only public search terms or public URLs and exclude private data from prompts and outputs.

## Reference(s):

- [Yicai homepage](https://www.yicai.com/)
- [ClawHub skill page](https://clawhub.ai/codekungfu/skills/yicai)
- [Publisher profile](https://clawhub.ai/user/codekungfu)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries, lists, statistics, and timelines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source links and collection timestamps for extracted public news items.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
