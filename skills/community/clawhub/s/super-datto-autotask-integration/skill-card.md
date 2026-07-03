## Description: <br>
Helps agents use the Membrane CLI to connect to Datto Autotask, discover or create actions, and run workflows for tickets, contacts, projects, records, reports, and automations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
IT service management teams and their agents use this skill to operate Datto Autotask through Membrane for ticket, contact, project, record, report, and automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify live Datto Autotask business records or trigger automations without clear safety boundaries. <br>
Mitigation: Use tenant-scoped, least-privilege Membrane connections; require explicit user approval before write actions; test on non-production or low-risk records before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-datto-autotask-integration) <br>
- [Membrane](https://getmembrane.com) <br>
- [Datto Autotask documentation](https://ww1.autotask.net/help/Content/home.htm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON command-output options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to use Membrane-managed connections and JSON output where useful.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
