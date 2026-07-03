## Description: <br>
Create, update, and publish websites with Revdoku buckets, including interactive app sites backed by a per-bucket server database, while storing files privately until the user asks for a public or protected link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emirn](https://clawhub.ai/user/emirn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to publish local folders or bucket files as Revdoku websites, including static sites, protected sites, and app sites with per-bucket database actions. It guides when to use the Revdoku CLI, MCP tools, or REST flows and when to require user confirmation for publishing or lifecycle actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish local folders live and may reuse saved Revdoku credentials. <br>
Mitigation: Use draft publishing until ready, verify publication status before sharing a live URL, and require explicit user confirmation for publish, unpublish, archive, restore, grant exchange, and permanent delete actions. <br>
Risk: The helper script can download and execute an unpinned Revdoku CLI. <br>
Mitigation: Review the helper script before first use and prefer an already installed or pinned Revdoku CLI when available. <br>
Risk: Published websites may include analytics or browser-side event tracking. <br>
Mitigation: Disable analytics or tracking when the user does not want those signals collected. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/emirn/revdoku) <br>
- [Revdoku app](https://app.revdoku.com) <br>
- [Revdoku app templates](https://github.com/revdoku/revdoku/tree/main/templates) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and implementation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to publish, draft, protect, unpublish, archive, restore, or delete Revdoku bucket content only with the user confirmations described by the skill.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
