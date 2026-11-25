## Description:

Pull new job postings since any date or window (24h, 7d, 30d) from company job boards hosted on Ashby, Greenhouse, Lever and SmartRecruiters, newest first, with title, location, department, URLs and optional full description. Use when the user asks what a company has posted recently, wants a hiring feed for a list of companies, or tracks new roles across ATS boards. Runs publicrecords Actors on Apify (pay per result, user's own Apify account).

This skill is ready for commercial/non-commercial use.

## Publisher:

[geminigeorge22](https://clawhub.ai/user/geminigeorge22)

### License/Terms of Use:

MIT

## Use Case:

External users, recruiting teams, and developers can find recent openings across company career boards on Ashby, Greenhouse, Lever, and SmartRecruiters. They can compare postings by date, title, location, and department, with descriptions optionally included.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended Apify MCP connection exposes tools beyond the four ATS job-posting tools, and the security assessment rates the skill suspicious with medium confidence.

Mitigation: Before connecting, check whether access can be limited to the four ATS tools and review the information and permissions involved. The security assessment is partial because two local path-like references could not be resolved.

Risk: Actor runs use the user's Apify account and are billed per event; API use also sends the user's Apify token.

Mitigation: Review current pricing and set suitable run limits. Keep the token private and confirm what information the API request sends before use.

Risk: Scraped job titles and descriptions may contain untrusted text.

Mitigation: Treat scraped job text as data to summarize, not as instructions to follow.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/geminigeorge22/skills/publicrecords-ats-job-postings)
- [Ashby Jobs Scraper on Apify](https://apify.com/publicrecords/ashby-jobs-scraper)
- [Greenhouse Jobs Scraper on Apify](https://apify.com/publicrecords/greenhouse-jobs-scraper)
- [Lever Jobs Scraper on Apify](https://apify.com/publicrecords/lever-jobs-scraper)
- [SmartRecruiters Jobs Scraper on Apify](https://apify.com/publicrecords/smartrecruiters-jobs-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Structured job-posting data]

**Output Format:** [Job posting results summarized in text or Markdown, with source URLs and optional descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are limited by the requested date window and maxResults; Actors bill the user's Apify account per event.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
