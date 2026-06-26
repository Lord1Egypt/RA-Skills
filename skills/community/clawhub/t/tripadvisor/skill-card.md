## Description: <br>
Find and compare Tripadvisor hotels, restaurants, and attractions with official API workflows, URL-first navigation, and policy-safe data handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Travel planners and agents use this skill to search Tripadvisor destinations, compare hotels, restaurants, and attractions, and produce ranked shortlists with transparent tradeoffs and uncertainty notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tripadvisor API requests can expose destination names, date windows, filters, and other travel context to Tripadvisor services. <br>
Mitigation: Use only the minimum travel context needed for the task and disclose whether the output used API, UI, or hybrid sources. <br>
Risk: The skill relies on TRIPADVISOR_API_KEY and request logging, which could expose credentials if copied into logs. <br>
Mitigation: Protect TRIPADVISOR_API_KEY and redact API keys from request logs, replacing secrets with [REDACTED]. <br>
Risk: Local files under ~/tripadvisor/ may retain travel preferences, blockers, request notes, and shortlists. <br>
Mitigation: Confirm the first write, store only reusable non-sensitive preferences and selected options, and review or delete ~/tripadvisor/ when local retention is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/tripadvisor) <br>
- [Skill homepage](https://clawic.com/skills/tripadvisor) <br>
- [Tripadvisor Content API location search](https://api.tripadvisor.com/api/partner/2.0/location/search) <br>
- [Tripadvisor website](https://www.tripadvisor.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with ranked shortlists, rationale, uncertainty notes, and inline shell commands when API workflows are used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should identify the source mode used, such as API, UI, or hybrid, and redact secrets in logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
