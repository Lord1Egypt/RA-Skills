## Description:

Turn seller-supplied restock facts and an already-written restock script into one talking clip per still.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and their agents use this skill to turn authorized still images, confirmed restock facts, and already-written lines into short talking restock announcement clips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package uses a shared Beatra credential with permissions that can spend credits and access account tasks or artifacts beyond a single clip job.

Mitigation: Install only if that account-level access is acceptable, review paid-operation prompts before approval, and revoke the connected device in the Beatra Console when it is no longer trusted.

Risk: Automatic code updates are enabled by default and run silently during normal client use.

Mitigation: Consider disabling automatic updates with `python3 scripts/mcp_client.py update --auto off`; use the documented update check or re-enable updates when appropriate.

Risk: Paid speech, voice-clone, and video steps can consume credits, and initial estimates may differ from final settled charges.

Mitigation: Confirm each paid stage separately, use unique request IDs for approved work, and report final `billing.net_charged_credits` from completed task results.

## Reference(s):

- [Restock talking workflow](artifact/references/workflow.md)
- [Installation and authentication](artifact/references/installation-and-auth.md)
- [Installation registration](artifact/references/installation-registration.md)
- [Tasks and results](artifact/references/tasks-and-results.md)
- [Billing, errors, and recovery](artifact/references/billing-errors-and-recovery.md)
- [Bundled MCP Client diagnostics](artifact/references/mcp-connection.md)
- [Automatic updates and safety](artifact/references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](artifact/references/uninstall-and-disconnect.md)
- [Beatra skill homepage](https://beatra.ai/skills/restock-drop-talking)
- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/restock-drop-talking)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON payload examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agent calls that may create Beatra speech, voice-clone, upload, wallet, task, and video outputs through the bundled client.]

## Skill Version(s):

0.1.2 (source: server release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
