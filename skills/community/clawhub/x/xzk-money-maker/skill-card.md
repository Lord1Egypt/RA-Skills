## Description: <br>
Fetches real-time part-time job and gig listings from the Kuaijiejian backend based on a user's earning or job-search request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heqq-github](https://clawhub.ai/user/heqq-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users ask for part-time work, gig work, or earning opportunities; the skill sends the request to the Kuaijiejian backend and returns matching listings with pay, time, location, and application links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Job-search prompts are sent to the Kuaijiejian backend and may contain personal details. <br>
Mitigation: Keep requests minimal and avoid phone numbers, identity documents, financial details, or full employment history. <br>
Risk: Returned listings may include pay claims and signup links that require user judgment. <br>
Mitigation: Verify compensation, schedule, location, and application links before applying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heqq-github/xzk-money-maker) <br>
- [Kuaijiejian skill API endpoint](https://test-gig-c-api.1haozc.com/api/wx/kjj/v1/customer/skill/call) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [Plain text or Markdown job listings with preserved backend links; JSON error objects on script failure.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves backend-provided signup and mini-program links on independent lines; script timeout is 30 seconds.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
