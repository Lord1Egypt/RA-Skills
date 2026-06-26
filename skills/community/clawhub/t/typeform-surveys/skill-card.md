## Description: <br>
Manage Typeform forms, responses, themes, workspaces, and webhooks via the Typeform API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage Typeform surveys from an agent, including form discovery, response review, form creation, themes, workspaces, and webhooks through a connected Typeform account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth-backed access to a connected Typeform account and may handle survey response data that contains personal information. <br>
Mitigation: Use only the intended connected account, keep access scoped to data the account is authorized to view, and handle response data according to privacy requirements. <br>
Risk: Write and delete operations can create forms, update settings, delete responses, or remove webhooks, and deleted Typeform data may not be recoverable. <br>
Mitigation: Preview and confirm write or delete actions before execution, and prefer read/list/get operations first when the target form, response, field, workspace, or webhook is ambiguous. <br>
Risk: The required ClawLink plugin uses sensitive credentials for hosted connection flows. <br>
Mitigation: Install the plugin only when ClawLink/Typeform workflows are expected, verify the Typeform connection before use, and report real tool errors instead of assuming missing capabilities. <br>


## Reference(s): <br>
- [ClawHub Typeform Skill](https://clawhub.ai/hith3sh/typeform-surveys) <br>
- [Publisher Profile](https://clawhub.ai/user/hith3sh) <br>
- [Typeform Developer Documentation](https://www.typeform.com/developers/) <br>
- [Typeform API Reference](https://www.typeform.com/developers/get-started) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the connected Typeform account through ClawLink; write and delete actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
