## Description: <br>
Onboard a new user to WhatsApp via WAHA--greet them, collect and sanitize their phone number, create/start a WAHA session, request and share a pairing code, verify authentication, and then offer next actions (recent chats, contacts, specific chat). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lotfinity](https://clawhub.ai/user/lotfinity) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect a WhatsApp account through WAHA by collecting a phone number, creating or starting a WAHA session, sharing a pairing code, checking authentication, and offering next WhatsApp actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill links a persistent WhatsApp session without clearly explaining account access, retention, or cleanup. <br>
Mitigation: Use only a trusted WAHA instance, confirm what WhatsApp data the agent may access after pairing, and make sure the user knows how to unlink or delete the WAHA session. <br>
Risk: The artifact derives WAHA session names directly from the user's phone number. <br>
Mitigation: Prefer an opaque session name instead of one containing the phone number. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lotfinity/waha-onboarding) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and user-facing instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides WAHA session creation, pairing-code sharing, authentication checks, and follow-up WhatsApp actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
