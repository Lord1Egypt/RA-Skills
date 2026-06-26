## Description: <br>
Searches ITviec, TopDev, ITJobs, and TopCV for recent full-stack developer job listings in Vietnam using Firecrawl, then summarizes deduplicated results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cngvc](https://clawhub.ai/user/cngvc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and job seekers use this skill to ask an agent for current Vietnam full-stack developer roles and receive a consistent, source-grouped report. It is suited to repeated job-search prompts involving React, Next.js, TypeScript, Node.js, NestJS, and related technologies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically uses Firecrawl-backed searches against public job sites, which can consume API quota or incur billing. <br>
Mitigation: Use a dedicated, revocable Firecrawl API key and monitor quota or billing during use. <br>
Risk: The skill depends on a separate firecrawl-search skill and the FIRECRAWL_API_KEY credential. <br>
Mitigation: Review the required firecrawl-search skill separately and scope the API key to the minimum access needed. <br>
Risk: Job results may be incomplete, duplicated, stale, or affected by external site availability. <br>
Mitigation: Review source links before acting on a listing and rerun searches when freshness matters. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cngvc/vietnam-fullstack-jobs) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text report in Vietnamese with source-grouped job listings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the firecrawl-search skill and a FIRECRAWL_API_KEY; deduplicates listings by job title and company.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
