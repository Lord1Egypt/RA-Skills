## Description: <br>
Use when a user is trying to discover an installable or reusable skill or workflow, especially when they ask for a skill for a task, want to compare nearby skill categories, or need help narrowing discovery results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[littledinoc](https://clawhub.ai/user/littledinoc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to discover installable or reusable skills, compare nearby skill categories, narrow ambiguous requests with one clarification, and return final skill recommendations backed by search results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skill-search queries and clarification details are sent to a third-party service. <br>
Mitigation: Use the skill only when the user is comfortable sending search intent to skills.megatechai.com, and avoid private repository names, secrets, customer data, or other sensitive project details. <br>
Risk: The skill requires feedback telemetry after final recommendations. <br>
Mitigation: Disclose the feedback step before use in sensitive contexts and keep feedback comments short, factual, and free of confidential information. <br>
Risk: The publisher does not provide a clear retention policy or opt-out path in the available evidence. <br>
Mitigation: Treat query, clarification, recommendation, and feedback data as shared with the third-party publisher unless stronger privacy terms are reviewed separately. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/littledinoc/skill-grep) <br>
- [Skill Grep service API](https://skills.megatechai.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown recommendations with structured API request and response JSON, plus optional shell installation commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns 1-3 skill recommendations after up to two retrieval passes and records final user feedback through the configured service.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
