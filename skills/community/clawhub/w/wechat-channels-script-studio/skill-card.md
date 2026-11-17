## Description:

Turns confirmed product facts into a WeChat Channels short-video script with a second-by-second segment table, full spoken narration, product-link beats, and a six-dimension draft score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, merchants, and marketing teams use this skill to turn confirmed facts about a product or service into a filmable WeChat Channels selling-video script, including a fact sheet, timed segment table, narration, link beats, and draft score. When explicitly requested, it can help produce storyboard frames and voiced narration through authenticated Beatra tools after user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package uses a shared full-scope local Beatra device token and can make authenticated Beatra MCP calls.

Mitigation: Install only when that account access is acceptable, keep the token in the local credential file, and revoke the device from the Beatra Console when the connection is no longer trusted or needed.

Risk: The bundled client can silently update package-owned files.

Mitigation: Review the package before installation and disable silent updates with `python3 scripts/mcp_client.py update --auto off` when automatic replacement is not desired.

Risk: Optional storyboard and speech generation can spend Beatra credits after approval.

Mitigation: Review paid-operation prompts, prices, request identifiers, and approved media inputs before allowing any generation call.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/wechat-channels-script-studio)
- [Beatra skill homepage](https://beatra.ai/skills/wechat-channels-script-studio)
- [Structuring the script](references/script-structure.md)
- [Placing the product-link beats](references/product-link-beats.md)
- [Script studio workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Bundled MCP Client diagnostics](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, prose narration, score summaries, and optional shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional Beatra task IDs, artifact links, media dimensions, narration duration, resolved model, and billing values when paid storyboard or speech artifacts are produced.]

## Skill Version(s):

0.1.4 (source: server release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
