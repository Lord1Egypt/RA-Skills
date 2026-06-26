## Description: <br>
Use the ClawRSS OpenClaw plugin to manage RSS feeds, persist web results, pull saved items, work with digest articles, and send Apple push notifications after the plugin is installed and enabled. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ipocket-app](https://clawhub.ai/user/ipocket-app) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to operate ClawRSS in a workspace: manage RSS feeds, save search and article results, pull and mark stored items, work with digest records, and send configured push notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClawRSS operations can delete feeds, mark saved items consumed, or save digest content in the active workspace. <br>
Mitigation: Confirm the workspace ID and user intent before write or destructive actions, then report the tools called and verification results. <br>
Risk: Push notification text may appear on connected Apple devices. <br>
Mitigation: Check push configuration when uncertain and keep notifications brief, factual, and user-approved. <br>
Risk: A normal webpage can be mistaken for a subscribable RSS or Atom feed. <br>
Mitigation: Subscribe only confirmed feed URLs and verify feed changes by listing feeds after an upsert or delete. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ipocket-app/use-clawrss) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, tool calls, markdown] <br>
**Output Format:** [Markdown responses with structured status summaries and ClawRSS tool-call arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the active workspace as the ClawRSS namespace and reports tools called, saved or changed records, verification results, and missing inputs.] <br>

## Skill Version(s): <br>
2026.3.29 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
