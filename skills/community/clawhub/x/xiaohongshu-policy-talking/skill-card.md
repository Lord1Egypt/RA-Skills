## Description:

Turn Xiaohongshu policy-question notes into one talking policy clip per still. This Xiaohongshu policy talking studio reads public policy-question notes, then records each already-written public-policy line as a 2 to 15s talking clip. Those policy talking clips stay separate files they can send on their own.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agency desks use this skill to turn public Xiaohongshu policy-question notes and already-written public-policy answers into short, separate talking clips. It guides the agent through note lookup, slot planning, speech generation, video generation, billing confirmation, and recovery without inventing policy facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a shared Beatra device credential that can spend credits and access Beatra tools.

Mitigation: Install and use it only when the Beatra account and credential trust model are acceptable, and require explicit confirmation before every paid lookup, clone, speech, video, cancellation, upload, or uninstall action.

Risk: The bundled client can silently replace package-owned executable files during automatic updates.

Mitigation: Review the package before installation and disable automatic updates for the installation when silent replacement is not acceptable.

Risk: The workflow may upload local media and use faces or voices for generated clips.

Mitigation: Use only media with appropriate likeness and voice rights, inspect files before upload, and avoid sensitive local media unless the destination and account trust model are acceptable.

Risk: Paid asynchronous requests can create duplicate charges if replayed with changed inputs or new request identities.

Mitigation: Use one opaque client_request_id per approved request, poll returned task IDs through terminal state, and retry only byte-identical uncertain submissions with the same request identity.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/beatra-ai/skills/xiaohongshu-policy-talking)
- [Beatra Skill Homepage](https://beatra.ai/skills/xiaohongshu-policy-talking)
- [Policy talking-clip workflow](artifact/references/workflow.md)
- [Xiaohongshu policy-question note lookup](artifact/references/note-lookup.md)
- [Installation and authentication](artifact/references/installation-and-auth.md)
- [Tasks and results](artifact/references/tasks-and-results.md)
- [Billing, errors, and recovery](artifact/references/billing-errors-and-recovery.md)
- [Automatic updates and safety](artifact/references/automatic-updates-and-safety.md)
- [Beatra MCP endpoint](https://mcp.beatra.ai/mcp)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Files, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks, plus generated media artifact references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 2 to 8 separate talking-clip outputs and related speech assets; paid lookup, speech, clone, upload, cancellation, uninstall, and video actions require explicit confirmation.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
