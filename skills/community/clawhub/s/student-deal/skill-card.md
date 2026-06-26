## Description: <br>
Find student flight discounts, under-26 fares and youth travel deals with student verification and budget airline tickets, powered by FlyAI/Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and travel shoppers use this skill to ask an agent for student-oriented flight searches, budget filters, flexible-date options, and booking-link summaries based on FlyAI CLI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install an unpinned global FlyAI CLI if it is missing. <br>
Mitigation: Manually review and approve any CLI installation first, and prefer an isolated or pinned environment. <br>
Risk: Trip details and search filters may be sent to the external FlyAI/Fliggy travel provider. <br>
Mitigation: Use the skill only when the user is comfortable sharing those travel details with the provider, and avoid submitting sensitive information unnecessarily. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FlyAI CLI output for flight data and should not answer from model memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
