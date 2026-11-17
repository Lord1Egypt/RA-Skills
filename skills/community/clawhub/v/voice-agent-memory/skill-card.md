## Description:

Full-stack voice agent with BlueColumn persistent memory. Make and receive phone calls with real-time transcription, automatic vector memory storage, and cross-call recall. Every call remembers who called, what they said, and what happened last time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a phone-based AI agent that recalls prior caller conversations, injects memory into responses, and stores new call context for future interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weak or missing authentication controls could expose caller memory and paid AI access.

Mitigation: Enforce rejection of invalid tokens before deployment and protect all call history, outbound call, and administrative endpoints.

Risk: Caller identity accepted from request metadata or prompt text could cause memory to be recalled or stored under the wrong caller.

Mitigation: Verify caller identity with the telephony provider before using a phone number for memory lookup or storage.

Risk: Automatic memory storage can retain call transcripts without clear caller consent.

Mitigation: Disable or gate automatic memory storage until consent, retention, and deletion controls are defined.

Risk: Public bridge exposure can increase access to caller memory and paid provider APIs.

Mitigation: Keep the bridge private or behind hardened access controls until authentication and endpoint protections are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/voice-agent-memory)
- [Publisher profile](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, configuration steps, and FastAPI bridge code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent setup guidance and bridge behavior for phone calls, transcription, memory recall, and memory storage.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
