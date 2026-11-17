## Description:

Turn already-written short sleep stories into one spoken clip per labeled story.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Producers use this skill to turn their own short sleep-story scripts into labeled bedtime narration clips, typically 8 to 20 MP3 reads, using a catalog voice or an authorized cloned voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad Beatra account authority for media, artifacts, tasks, and billing-related actions.

Mitigation: Install and authorize it only when that access is acceptable, keep the local device token private, and revoke the Beatra device authorization when the skill is no longer needed.

Risk: The bundled client silently checks for and installs verified package updates by default.

Mitigation: Use the documented update command to disable automatic checks when change control is required, and re-enable or run manual checks after reviewing the release.

Risk: Paid clone and speech requests can create billing exposure if a task is retried with changed arguments or without preserving request identity.

Mitigation: Confirm each paid stage separately, use one opaque client request ID per submitted task, and retry uncertain submissions only with byte-identical arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/sleep-story-voice)
- [Beatra skill homepage](https://beatra.ai/skills/sleep-story-voice)
- [Sleep story workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Bundled MCP Client diagnostics](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with labeled clip lists, JSON payloads, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce one MP3 task per story slot through Beatra after user approval; clone and speech stages use separate request identities.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
