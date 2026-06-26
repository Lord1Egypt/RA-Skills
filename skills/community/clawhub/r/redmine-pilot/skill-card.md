## Description: <br>
Redmine Pilot helps agents query Redmine issues, create or update tickets, list projects, and retrieve Redmine metadata through the Redmine REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zer07z](https://clawhub.ai/user/zer07z) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, project managers, and support teams use this skill to inspect and manage Redmine project tickets from an agent workflow, including issue lookup, creation, status updates, and project metadata retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify live Redmine tickets when configured with an API key, and broad project-management triggers can cause accidental use. <br>
Mitigation: Use a least-privilege Redmine API key, keep prompts Redmine-specific, and require the agent to show the exact project, issue, fields, notes, and status changes before create or update actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zer07z/redmine-pilot) <br>
- [Redmine data structure example](artifact/references/schema-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples and JSON or text output from Redmine API commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDMINE_URL and REDMINE_API_KEY; configured commands can read, create, and update live Redmine issues.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
