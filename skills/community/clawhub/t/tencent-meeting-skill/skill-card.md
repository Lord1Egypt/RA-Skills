## Description:

腾讯会议 provides an agent with Tencent Meeting workflows for scheduling, updating, canceling, searching, and controlling meetings, plus participant, invitee, waiting-room, recording, transcript, smart-minutes, Yuanbao-minutes, contact-resolution, permission-request, version-check, and feedback actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wemeeting](https://clawhub.ai/user/wemeeting)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external Tencent Meeting users use this skill to manage meetings, attendees, recordings, transcripts, minutes, and meeting-related permissions from an agent. Developers and operators can also use it to route Tencent Meeting MCP tool calls through a local Python command wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can manage Tencent meetings, access meeting-derived content, resolve enterprise contacts for meeting actions, and change participant state.

Mitigation: Install only with a Tencent Meeting token scoped for those abilities, confirm sensitive meeting changes with the user, and avoid using contact tools for general personnel lookup.

Risk: The update flow can execute an installation from a server-provided address when auto-upgrade has been enabled.

Mitigation: Leave auto-upgrade disabled unless the remote update channel is trusted, review update prompts manually, and validate new artifacts before use.

Risk: Meeting topics, participants, contact details, recordings, transcripts, and feedback may contain sensitive information.

Mitigation: Apply the bundled privacy rules: minimize disclosure, mask phone numbers and email addresses, and require explicit user confirmation before submitting feedback or permission requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wemeeting/skills/tencent-meeting-skill)
- [Publisher Profile](https://clawhub.ai/user/wemeeting)
- [Tencent Meeting](https://meeting.tencent.com/)
- [Tencent Meeting MCP Token Endpoint](https://mcp.meeting.tencent.com/mcp/wemeet-open/v1)
- [API References](artifact/references/api_references.md)
- [Error Dictionary](artifact/references/error_dictionary.md)
- [Version Management](artifact/references/version_management.md)
- [Privacy Policy](artifact/references/privacy_policy.md)
- [Feedback Rules](artifact/references/feedback_rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown and text guidance with JSON-formatted MCP tool arguments and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and TENCENT_MEETING_TOKEN; calls the Tencent Meeting MCP endpoint configured in the artifact.]

## Skill Version(s):

1.0.15 (source: server release evidence and artifact config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
