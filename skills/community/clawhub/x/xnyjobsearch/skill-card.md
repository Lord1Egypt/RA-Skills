## Description:

Searches Hsolar/碳索人才网 renewable-energy job listings by keyword, location, industry, and page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gengzhw](https://clawhub.ai/user/gengzhw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn natural-language job-search requests into Hsolar API filters and present renewable-energy job listings in Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Job-search keywords, locations, industry filters, and pagination values are sent to the Hsolar/碳索人才网 API.

Mitigation: Avoid entering sensitive personal details in search terms; use general role, location, and industry filters.

Risk: Returned listings are sourced from an external job-search service and may change over time.

Mitigation: Review listing details on Hsolar before relying on a posting or applying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gengzhw/skills/xnyjobsearch)
- [Hsolar job search API endpoint](https://openapi.hsolar.com/Api/V1.0/Search/Jobsv2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown table with job listing summaries and pagination metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are filtered by keyWord, location, industry, pageIndex, and pageSize; pageSize is capped at 50.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
