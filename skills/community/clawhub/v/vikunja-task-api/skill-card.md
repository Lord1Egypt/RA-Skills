## Description: <br>
Full Vikunja v2 API integration for projects, tasks, labels, teams, views, comments, attachments, bulk operations, and related task-management workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashanzzz](https://clawhub.ai/user/ashanzzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect an agent to a Vikunja instance and manage task-management data through documented API calls and the included CLI helper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate on real Vikunja data, including deletes, bulk edits, sharing, and membership changes. <br>
Mitigation: Use it only for intended Vikunja management workflows and review delete, share, bulk update, and rights-change commands before execution. <br>
Risk: Credentials may be persisted insecurely if users follow shell-profile examples. <br>
Mitigation: Use a least-privileged Vikunja API token and store secrets in OpenClaw's secure environment handling or a secret manager instead of shell startup files. <br>
Risk: An unpinned remote helper-script install command could fetch changed content later. <br>
Mitigation: Prefer the packaged helper script included with the release artifact. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ashanzzz/vikunja-task-api) <br>
- [Vikunja](https://vikunja.io/) <br>
- [Vikunja Filters Documentation](https://vikunja.io/docs/filters/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VIKUNJA_URL plus either VIKUNJA_TOKEN or VIKUNJA_USERNAME and VIKUNJA_PASSWORD; helper script depends on curl and jq.] <br>

## Skill Version(s): <br>
2.5.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
