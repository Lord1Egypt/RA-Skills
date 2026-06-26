## Description: <br>
Job search and career discovery through your agent. Find tech companies that match your stack, star the ones you'd actually work for, and pull remote developer jobs from your shortlist, all by talking. Backed by company-level tech stack data nobody else has. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[remoet](https://clawhub.ai/user/remoet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and job seekers use this skill to find technology companies that match their stack, curate a starred company shortlist, manage a Remoet profile, and retrieve jobs from companies they have already vetted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send professional profile details, CV-derived work history, projects, education, saved jobs, application notes, and messages to Remoet. <br>
Mitigation: Review and redact sensitive CV or profile content before asking the agent to import it, and only connect the skill when sharing that information with Remoet is acceptable. <br>
Risk: Changing visibility can make the user's profile discoverable to companies on the platform. <br>
Mitigation: Keep visibility set to NONE unless the user intentionally chooses STARRED or ALL visibility after understanding who can discover the profile. <br>
Risk: Some job actions affect applications, messages, saved jobs, stars, or subscription state. <br>
Mitigation: Confirm user intent before applying, withdrawing, accepting or rejecting offers, messaging companies, changing stars, or starting an upgrade flow. <br>


## Reference(s): <br>
- [Remoet homepage](https://remoet.dev) <br>
- [Remoet onboarding](https://remoet.dev/onboarding?utm_source=clawhub) <br>
- [ClawHub Remoet skill page](https://clawhub.ai/remoet/remoet) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON or YAML configuration snippets, and MCP tool-use instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Remoet API key or OAuth-capable MCP client; tool results may include profile, company, job, application, digest, subscription, and link tree data.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
