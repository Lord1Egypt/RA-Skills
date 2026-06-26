## Description: <br>
Search Bangladesh government jobs from the Teletalk AllJobs API, filter out excluded keywords, present matching jobs, and track applied job IDs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sazidulalam47](https://clawhub.ai/user/sazidulalam47) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search and shortlist Bangladesh government job listings from Teletalk AllJobs, excluding unwanted job-title keywords and tracking jobs they have applied to. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads live job data from an external Teletalk AllJobs endpoint, so results may be incomplete, unavailable, or changed after retrieval. <br>
Mitigation: Confirm important deadlines and application details on the official application site before acting. <br>
Risk: The skill stores search preferences and applied job IDs in local data files. <br>
Mitigation: Review the local data files before sharing the skill folder or generated reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sazidulalam47/teletalk-alljobs-govjob-search) <br>
- [Publisher profile](https://clawhub.ai/user/sazidulalam47) <br>
- [Teletalk AllJobs search API](https://alljobs.teletalk.com.bd/api/v1/published-jobs/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with JSON job-list output from the search script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script filters out expired deadlines and excluded keywords, then returns compact job records with titles, organization names, vacancies, deadlines, application URLs, and job IDs.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
