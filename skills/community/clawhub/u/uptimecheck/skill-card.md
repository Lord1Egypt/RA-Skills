## Description: <br>
Check if URLs and API endpoints are up or down with response times and status codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogue-agent1](https://clawhub.ai/user/rogue-agent1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check URL and API endpoint availability, measure response time, review recent check history, and get CI-friendly exit codes for uptime checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network requests to URLs supplied by the user. <br>
Mitigation: Use it only with endpoints the user intends to contact, and avoid sensitive internal URL lists unless that monitoring is deliberate. <br>
Risk: Saved history can include endpoint names, timestamps, status codes, and response times in the user's home directory. <br>
Mitigation: Use --save only when local storage of this check history is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rogue-agent1/uptimecheck) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and JSON Lines history records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print endpoint status, response time, summaries, and optional saved check history.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
