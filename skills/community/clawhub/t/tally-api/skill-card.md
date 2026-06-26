## Description: <br>
Tally API integration with managed OAuth for managing forms, submissions, workspaces, webhooks, organization users, and organization invites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Tally account resources through Maton-managed OAuth, including forms, submissions, workspaces, webhooks, organization users, and invites. It is useful when an agent needs to generate API calls, examples, or operational guidance for Tally workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Maton API key and OAuth-backed access to a connected Tally account. <br>
Mitigation: Keep MATON_API_KEY in the environment or a secrets manager, avoid exposing it in logs, and verify the intended Tally connection before use. <br>
Risk: Write operations can create, update, or delete forms, workspaces, submissions, webhooks, organization users, and invites. <br>
Mitigation: Confirm the target resource and intended effect with the user before every create, update, delete, invite, removal, or retry operation. <br>
Risk: Webhooks can transmit form submission data, including personal or sensitive respondent information, to external URLs. <br>
Mitigation: Confirm the destination URL, form, and event types before creating or updating webhooks. <br>
Risk: Scanner telemetry is clean, but the security evidence notes that the target skill files were not available for full artifact review. <br>
Mitigation: Inspect the visible skill instructions and requested permissions before installation or deployment. <br>


## Reference(s): <br>
- [ClawHub Tally Skill Page](https://clawhub.ai/byungkyu/tally-api) <br>
- [Tally API Introduction](https://developers.tally.so/api-reference/introduction) <br>
- [Tally API Reference](https://developers.tally.so/llms.txt) <br>
- [Tally Help Center](https://help.tally.so/) <br>
- [Maton Settings](https://maton.ai/settings) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash, Python, JavaScript, HTTP examples, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a Tally OAuth connection; write operations require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
