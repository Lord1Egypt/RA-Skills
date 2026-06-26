## Description: <br>
快结荐兼职赚钱平台 forwards job-search or income-related prompts to the 快结荐 backend API and returns real-time job or gig listings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heqq-github](https://clawhub.ai/user/heqq-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to ask for part-time jobs, gig work, day-labor roles, recruiting opportunities, or income opportunities. The agent sends the user's prompt to the 快结荐 service and formats the returned listings, compensation, schedules, locations, and application links for the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Job-search or income-related prompts are sent to an external 快结荐 backend service. <br>
Mitigation: Avoid sending contact details, ID numbers, exact addresses, salary history, or other sensitive personal information unless the user trusts that service. <br>
Risk: Returned listings, compensation, locations, schedules, and application links come from the external service. <br>
Mitigation: Present returned opportunities clearly and encourage users to verify job details before applying or sharing personal information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heqq-github/zxk-money-maker) <br>
- [Publisher profile](https://clawhub.ai/user/heqq-github) <br>
- [快结荐 skill API endpoint](https://test-gig-c-api.1haozc.com/api/wx/kjj/v1/customer/skill/call) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown summary of JSON job-listing results or JSON-formatted error details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include compensation, schedule, location, and plain-text mini-program application links returned by the external service.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
