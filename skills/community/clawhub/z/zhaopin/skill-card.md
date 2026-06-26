## Description: <br>
Helps agents summarize public Zhaopin job listings and company pages, including role details, salary, experience, education, benefits, and company attributes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to inspect public Zhaopin search results, job detail pages, and company pages, then produce concise summaries and comparisons for job-market analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be misused to automate login, job applications, verification bypass, or access to non-public account data. <br>
Mitigation: Use it only for public Zhaopin pages and keep login, application submission, and non-public account workflows out of scope. <br>
Risk: Repeated or large-scale collection could violate platform rules or create operational risk. <br>
Mitigation: Keep usage lightweight, avoid bulk scraping, respect platform rules, and prefer human-opened pages when dynamic rendering or verification appears. <br>
Risk: Job listing details can become stale or misleading if reused without context. <br>
Mitigation: Include the collection time and source link in summaries so readers can verify current listing details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CodeKungfu/zhaopin) <br>
- [Zhaopin home page](https://www.zhaopin.com/) <br>
- [Zhaopin job search](https://sou.zhaopin.com/) <br>
- [Publisher profile](https://clawhub.ai/user/CodeKungfu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries or structured text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on public pages and should include collection time when reporting job data.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
