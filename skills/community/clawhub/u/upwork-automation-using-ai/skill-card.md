## Description: <br>
Automates Upwork login, job search, filtering, and proposal drafting in one browser session, stopping before submission unless explicitly instructed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adeel-powerhouse](https://clawhub.ai/user/adeel-powerhouse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Freelancers or operators using an agent-controlled browser use this skill to search Upwork against explicit criteria, shortlist suitable jobs, draft proposal fields, and stop for human review before submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent operates an active Upwork browser session, including login flows. <br>
Mitigation: Prefer manual login where possible, provide credentials only for the active run, and do not persist credentials. <br>
Risk: Job selection or proposal content could be incorrect or misaligned with visible job requirements. <br>
Mitigation: Review selected jobs, criteria matches, and filled proposal fields before relying on the result. <br>
Risk: A proposal could be submitted before the user has verified the final content. <br>
Mitigation: The skill stops before submission and requires explicit approval after final review. <br>


## Reference(s): <br>
- [Proposal Template](references/proposal-template.md) <br>
- [Session Checklist](references/session-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown status summary and drafted proposal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stops before submission unless the user explicitly says submit now.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
