## Description:

Provides agent guidance for automating Tencent Exmail Web through Kimi WebBridge, including iframe navigation, text encoding, mail reading, reply, reply-all, forwarding, draft editing, and folder navigation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolingrabbit](https://clawhub.ai/user/coolingrabbit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate Tencent Exmail Web in an already logged-in browser session through Kimi WebBridge. It helps read mail, prepare replies, reply-all messages, forwards, body edits, drafts, and folder navigation while keeping sensitive mailbox actions under user review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mailbox automation can affect sensitive messages, recipients, subjects, and message bodies.

Mitigation: Require user review of recipients, subject, and body before saving drafts or sending any message.

Risk: Reply-all, forwarding, recipient edits, and sending can disclose email content to unintended recipients.

Mitigation: Require explicit user approval before reply-all, forwarding, recipient changes, or sending.

Risk: Untrusted text used as formatted HTML can alter draft content or rendering.

Mitigation: Avoid using untrusted text as formatted HTML; encode inserted text using the documented character-code approach.

Risk: The security summary identifies under-scoped draft, recipient, and body modification guidance.

Mitigation: Treat draft and body changes as proposals until the user confirms the final draft state.

## Reference(s):

- [Tencent Exmail WebBridge Reference](REFERENCE.md)
- [Tencent Exmail WebBridge README](README.md)
- [ClawHub skill page](https://clawhub.ai/coolingrabbit/skills/tencent-exmail-webbridge)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown instructions with JavaScript and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; produces operating guidance for a logged-in Tencent Exmail browser session.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and config list 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
