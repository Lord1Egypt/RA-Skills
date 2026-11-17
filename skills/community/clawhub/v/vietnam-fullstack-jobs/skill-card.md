## Description:

Searches ITviec, TopDev, ITJobs, and TopCV for current full-stack developer job listings using Firecrawl, with focus on React, Next.js, TypeScript, Node.js, NestJS, and related technologies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cngvc](https://clawhub.ai/user/cngvc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and job seekers use this skill to have an agent search Vietnam-focused job boards for full-stack roles and return a consistent, deduplicated list of listings. It is intended for requests such as finding new full-stack jobs or developer roles involving React, Next.js, TypeScript, Node.js, or NestJS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad prompts such as "job moi" may trigger external job searches and consume Firecrawl API quota.

Mitigation: Install and enable the skill only where Vietnam job-search prompts are expected, and monitor Firecrawl API usage.

Risk: Job listings returned from public sites may be stale, duplicated, incomplete, or unavailable during scraping.

Mitigation: Treat results as leads for review, preserve source URLs in the output, and deduplicate by title and company before presenting results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cngvc/skills/vietnam-fullstack-jobs)
- [Artifact README](artifact/README.md)
- [Artifact Skill Instructions](artifact/SKILL.md)
- [ITviec Full-Stack Jobs](https://itviec.com/it-jobs/full-stack)
- [TopDev Fullstack Search](https://topdev.vn/jobs?q=fullstack)
- [ITJobs Fullstack Search](https://www.itjobs.com.vn/vi/search?Keyword=fullstack)
- [TopCV Fullstack Developer Search](https://www.topcv.vn/tim-viec-lam-lap-trinh-vien-fullstack)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text in Vietnamese with grouped job listings and URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the firecrawl-search skill and FIRECRAWL_API_KEY; deduplicates listings by job title and company.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
