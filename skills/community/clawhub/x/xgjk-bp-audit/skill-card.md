## Description: <br>
XGJK BP Audit helps agents audit BP goal systems across baseline compliance, upward alignment, downward handoff, gap analysis, and numerical alignment using BP Open-API data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[houtonghoutong](https://clawhub.ai/user/houtonghoutong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business planning reviewers, operations teams, and agent users use this skill to inspect organizational or individual BP goals, key results, actions, alignment paths, ownership, and numerical definitions. It can also propose and, with explicit approval, create child key results or actions through the BP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use credential-backed write actions to create BP key results or actions in a production BP system. <br>
Mitigation: Treat audit workflows as read-only by default and require explicit final approval after showing the exact parent ID and payload before running add_key_result or add_action. <br>
Risk: An exposed or over-privileged appKey could allow unintended BP API access. <br>
Mitigation: Use a least-privilege appKey, keep it only in environment variables or memory, and never place it in chat logs or files. <br>
Risk: Changing BP_OPEN_API_BASE_URL could direct credentialed requests to an untrusted host. <br>
Mitigation: Use the documented BP API base URL unless the deployment owner has verified the alternate host. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/houtonghoutong/xgjk-bp-audit) <br>
- [BP audit API index](openapi/bp-audit/api-index.md) <br>
- [Authentication and authorization rules](common/auth.md) <br>
- [BP audit usage examples](examples/bp-audit/README.md) <br>
- [Quality audit rules](references/quality-rules.md) <br>
- [Upward alignment rules](references/upward-check-rules.md) <br>
- [Downward handoff rules](references/downward-check-rules.md) <br>
- [Gap analysis rules](references/gap-analysis-rules.md) <br>
- [Numerical audit rules](references/numerical-audit-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown audit reports with tables, evidence citations, recommendations, and optional shell commands for BP API actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses compact Markdown API output by default; raw JSON is reserved for cases where the user explicitly needs it.] <br>

## Skill Version(s): <br>
3.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
