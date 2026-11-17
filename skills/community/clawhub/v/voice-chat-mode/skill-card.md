## Description:

在用户明确要求中文语音聊天或中文语音模式时激活。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liang9886703](https://clawhub.ai/user/liang9886703)

### License/Terms of Use:

MIT-0

## Use Case:

External users enable this skill when they want the agent to reply in natural spoken Chinese for voice chat, TTS, or voice-model handoff. It rewrites responses into concise conversational speech with optional local emotion tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: While enabled, the skill continues formatting replies as spoken Chinese, which may be unexpected when the user wants normal written responses.

Mitigation: Use the documented disable phrases, such as "文字回答" or "别语音了", when normal written replies are desired.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text with optional inline emotion tags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, data access, or shell commands; the mode persists until disabled by a user phrase.]

## Skill Version(s):

0.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
