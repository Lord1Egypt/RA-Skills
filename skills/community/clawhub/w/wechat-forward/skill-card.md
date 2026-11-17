## Description:

Forwards the current conversation or selected content to the user's own WeChat account through wxclawbot only after an explicit WeChat forwarding request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidchyi-beep](https://clawhub.ai/user/davidchyi-beep)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send a concise copy or summary of current chat content to their own WeChat account for mobile reading. The skill is intended for explicit, user-requested forwarding only, not scheduled pushes, alerts, or automatic summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Message text or file paths could be handled unsafely if copied directly into a shell command.

Mitigation: Invoke wxclawbot with safe argument handling and avoid pasting raw untrusted text or paths into shell commands.

Risk: Untrusted or copied content could be forwarded to WeChat without adequate review.

Mitigation: Use the skill only after an explicit user request, verify the destination is the user's own WeChat account, and review content before forwarding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davidchyi-beep/skills/wechat-forward)
- [Publisher profile](https://clawhub.ai/user/davidchyi-beep)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, wxclawbot, and configured WeChat account credentials; sends only to the user's own WeChat account after explicit request.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
