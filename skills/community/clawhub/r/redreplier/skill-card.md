## Description: <br>
Monitor Reddit, Hacker News, X, and Bluesky for product or website keyword mentions with the RedReplier API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tarasshyn](https://clawhub.ai/user/tarasshyn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who manage product monitoring use this skill to configure RedReplier websites and keywords, retrieve and filter AI-scored mentions, triage leads, and manage alert settings through the RedReplier API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a RedReplier API token. <br>
Mitigation: Use a dedicated, revocable API token and keep REDREPLIER_API_KEY scoped to the agent runtime. <br>
Risk: Activating pending keywords can charge for a plan upgrade. <br>
Mitigation: Call the activation preview first, show the charge and target plan to the user, and require explicit confirmation before activation. <br>
Risk: Deleting a monitored website stops monitoring for that website. <br>
Mitigation: Confirm deletion with the user using the website domain, not only the resource ID. <br>


## Reference(s): <br>
- [RedReplier homepage](https://redreplier.com) <br>
- [ClawHub skill page](https://clawhub.ai/tarasshyn/redreplier) <br>
- [RedReplier API Reference](references/api-reference.md) <br>
- [RedReplier Mention Filtering](references/mention-filtering.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with curl commands and API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDREPLIER_API_KEY; paid keyword activation and website deletion require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
