## Description: <br>
搜索碳索人才网上的职位，支持按关键词、地点和行业过滤。新能源垂直行业招聘平台 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gengzhw](https://clawhub.ai/user/gengzhw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers, recruiters, and agents use this skill to search新能源 job listings on 碳索人才网 by keyword, location, industry, and page. It converts natural-language job-search requests into API parameters and returns readable Markdown results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search terms and filters to an external job-search API and returns third-party job listings that may be incomplete, outdated, or inaccurate. <br>
Mitigation: Avoid sensitive personal data in search terms, and verify listings through the linked source pages before making hiring or application decisions. <br>
Risk: Security guidance notes that related maintainer workflows may use existing service or model CLI credentials when invoked. <br>
Mitigation: Review commands before approving privileged actions, especially on private code or accounts. <br>


## Reference(s): <br>
- [xnyjobsearch on ClawHub](https://clawhub.ai/gengzhw/xnyjobsearch) <br>
- [碳索人才网 job search API endpoint](https://openapi.hsolar.com/Api/V1.0/Search/Jobsv2) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Text, Guidance] <br>
**Output Format:** [Markdown tables and summaries derived from JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search requests include keyword, location, industry, page index, and page size.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
