## Description:

Sends local files, URLs, or reusable Telegram file_ids into a Telegram chat via the Telegram Bot API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangwllu](https://clawhub.ai/user/wangwllu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deliver local files, URLs, or reusable Telegram file_ids to a Telegram chat or topic from an agent workflow. It is for file delivery, not normal assistant chat replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload any local file readable by the agent to Telegram.

Mitigation: Verify the file path and intended recipient before execution, and restrict the agent's filesystem access where possible.

Risk: The skill can auto-discover bot credentials and chat context without an explicit confirmation step.

Mitigation: Prefer explicit --chat-id and --topic-id values, store bot tokens in an environment secret manager or restricted-permission file, and avoid passing tokens on the command line.

Risk: Unpinned runtime dependencies may change behavior over time.

Mitigation: Pin python-telegram-bot and other dependencies in the deployment environment.

## Reference(s):

- [Telegram Bot API File Sending Reference](references/api_reference.md)
- [OpenClaw](https://github.com/wangwllu/openclaw)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [ClawHub Skill Page](https://clawhub.ai/wangwllu/skills/telegram-send-file)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with inline bash commands and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends selected files through Telegram and may return delivery status, message IDs, file IDs, or error text.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
