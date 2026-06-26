## Description: <br>
Production-oriented Vikunja task/project management skill with deterministic commands and strong validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KohlHammond](https://clawhub.ai/user/KohlHammond) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage Vikunja tasks, projects, comments, labels, assignees, views, webhooks, attachments, filters, notifications, subscriptions, and API tokens from deterministic shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate on live Vikunja data, including task edits, bulk updates, webhook creation, attachment transfer, subscriptions, and API token management. <br>
Mitigation: Use a least-privilege VIKUNJA_TOKEN, review commands before execution, and run the smoke test only against a test workspace. <br>
Risk: Creating API tokens or webhooks can expose sensitive access or send events to untrusted endpoints. <br>
Mitigation: Avoid shared logs when creating tokens and create webhooks only for trusted target URLs. <br>
Risk: Attachment upload and download commands read and write local file paths. <br>
Mitigation: Review attachment file paths before upload or download and prefer temporary test files during validation. <br>


## Reference(s): <br>
- [Vikunja project site](https://vikunja.io/) <br>
- [ClawHub skill release](https://clawhub.ai/KohlHammond/vikunja-complete) <br>
- [Publisher profile](https://clawhub.ai/user/KohlHammond) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, VIKUNJA_URL, and VIKUNJA_TOKEN.] <br>

## Skill Version(s): <br>
4.0.0 (source: release evidence; bundled CLI and changelog report 0.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
