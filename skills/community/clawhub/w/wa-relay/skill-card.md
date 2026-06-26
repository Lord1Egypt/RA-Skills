## Description: <br>
WA Relay routes third-party WhatsApp messages through an owner-controlled relay so an OpenClaw agent notifies the owner, logs conversations, and sends replies only after explicit owner instruction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zarruk](https://clawhub.ai/user/zarruk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to mediate WhatsApp interactions between an OpenClaw agent and non-owner contacts, keeping inbound messages routed to the owner and outbound replies gated on explicit owner instruction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose or retain privacy-sensitive WhatsApp communications through relaying, transcription, forwarding, and logs. <br>
Mitigation: Install only when that handling is acceptable, minimize or periodically purge wa-relay-log.md, and avoid retaining sensitive personal or business information longer than needed. <br>
Risk: A misconfigured owner number or ambiguous outbound instruction could send information to the wrong WhatsApp contact or group. <br>
Mitigation: Verify the owner WhatsApp number before use and require clear confirmation before outbound or group messages unless the owner has explicitly waived confirmation. <br>


## Reference(s): <br>
- [WA Relay examples](references/examples.md) <br>
- [ClawHub release page](https://clawhub.ai/zarruk/wa-relay) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown instructions with WhatsApp relay rules, message templates, and examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The hosting agent may maintain memory/wa-relay-log.md with relayed conversation history when following the skill instructions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
