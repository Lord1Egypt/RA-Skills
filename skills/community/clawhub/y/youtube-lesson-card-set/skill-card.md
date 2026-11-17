## Description:

Turn public YouTube lesson captions into a set of 4 to 8 takeaway cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers, instructional designers, and agents assisting them use this skill to turn public YouTube lesson captions or pasted lesson lines into concise takeaway-card plans and generation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shared Beatra device token grants broad media, wallet, artifact, and task permissions.

Mitigation: Review the requested access before installation and revoke the device from the Beatra Console or bundled uninstall flow when disconnecting.

Risk: Executable package code silently self-updates by default.

Mitigation: Disable automatic updates with `python3 scripts/mcp_client.py update --auto off` when approval is required before package code changes.

Risk: Caption lookup and image generation can consume Beatra credits.

Mitigation: Use the skill's confirmation cards, live price reads, and stable `client_request_id` recovery flow before submitting paid work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/youtube-lesson-card-set)
- [Beatra skill page](https://beatra.ai/skills/youtube-lesson-card-set)
- [Lesson knowledge-point still workflow](references/workflow.md)
- [YouTube lesson caption lookup](references/caption-lookup.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Tasks and results](references/tasks-and-results.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)
- [MCP connection](references/mcp-connection.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces caption-backed slot lists, confirmation cards for paid work, task recovery guidance, and delivery notes for generated card artifacts.]

## Skill Version(s):

0.1.3 (source: release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
