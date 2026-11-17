---
name: slack-free
slug: slack-free
displayName: "Slack"
version: "1.0.0"
summary: "经slack工具从SkillHub控Slack,含消息反应"
description: "经slack工具从SkillHub控Slack,含消息反应。The `slack` skill provides a comprehensive set of functionalities to control Slack from SkillHub, in。适用于多种工作场景,提供专业的能力支持。"
license: "MIT"
tools:
  - read
---

> **核心功能**: 本技能提供专业的能力支持等能力。


# Slack

## Overview

The `slack` skill provides a comprehensive set of functionalities to control Slack from SkillHub, including message reactions, message management, pinning/unpinning messages, and retrieving member information. This skill is ideal for automating workflows and enhancing team communication.

## Inputs to Collect

To use the `slack` skill, you need to provide the following inputs:

- `channelId`: The ID of the Slack channel where the action should be performed.
- `messageId`: The ID of the Slack message to be targeted (e.g., a message timestamp).
- `emoji`: An emoji to react to a message (in Unicode format or using Slack emoji names).
- `to`: The target for sending messages, specified as `channel:<id>` or `user:<id>`.
- `content`: The content of the message to be sent, edited, or deleted.
- `userId`: The ID of the Slack user whose information you want to retrieve.

## Actions

### Action Groups

The `slack` skill offers the following action groups:

- `reactions`: Manage reactions to messages.
- `messages`: Read, send, edit, and delete messages.
- `pins`: Pin and unpin messages.
- `memberInfo`: Retrieve information about Slack members.
- `emojiList`: List custom emoji in Slack.

### React to a Message

To react to a message, provide the `channelId`, `messageId`, and `emoji`. Here's an example:

```json
{
  "action": "react",
  "channelId": "C123",
  "messageId": "1712023032.1234",
  "emoji": "✅"
}
```

### Send a Message

To send a message, specify the `to` target and `content`. Here's an example:

```json
{
  "action": "sendMessage",
  "to": "channel:C123",
  "content": "Hello from SkillHub"
}
```

### Pin a Message

To pin a message, provide the `channelId` and `messageId`. Here's an example:

```json
{
  "action": "pinMessage",
  "channelId": "C123",
  "messageId": "1712023032.1234"
}
```

### List Pinned Items

To list pinned items in a channel, provide the `channelId`. Here's an example:

```json
{
  "action": "listPins",
  "channelId": "C123"
}
```

### Retrieve Member Information

To retrieve information about a Slack member, provide the `userId`. Here's an example:

```json
{
  "action": "memberInfo",
  "userId": "U123"
}
```

### List Custom Emoji

To list custom emoji in Slack, use the `emojiList` action. Here's an example:

```json
{
  "action": "emojiList"
}
```

## Ideas to Try

- Use the `react` action to mark completed tasks with a checkmark emoji.
- Pin important decisions or weekly status updates for easy reference.

## Dependency Requirements

### Runtime Environment

- **Agent Platform**: Any AI Agent that supports SKILL.md, such as  Code, Cursor, Codex, or  CLI.
- **Operating System**: Windows, macOS, or Linux.

### Dependencies

| Dependency | Type | Required | Source |
|:-----------|:-----|:---------|:-------|
| LLM API | API | Required | Provided by the Agent's built-in LLM |

### API Key Configuration

- The `slack` skill uses Markdown instructions and does not require an additional API key unless specified for external APIs.

### Usability Classification

- **Category**: MD+execute(Markdown instructions with some exec command-line execution capabilities)
- **Description**: A Markdown-based AI Skill that drives Agent execution through natural language instructions.

## Core Capabilities

- React to messages
- Manage pins
- Send, edit, and delete messages
- Fetch member information

## Use Cases

| Scenario | Input | Output |
|:--------|:------|:-------|
| Message reaction | Channel ID, Message ID, Emoji | Reaction added to the message |
| Message management | Channel ID, Message ID, Content | Message sent, edited, or deleted |
| Pinning | Channel ID, Message ID | Message pinned or unpinned |
| Member information retrieval | User ID | Member information retrieved |

**Not applicable for**: Complex decision scenarios requiring human judgment.

## Usage Process

1. Confirm that the runtime environment meets the requirements outlined in the dependency section.
2. Choose the appropriate usage method 基于 the applicable scenarios.
3. Execute the operation and verify the output result.
4. In case of errors, refer to the troubleshooting section.

## Examples

### Example 1: React to a Message

```plaintext
Input: User requests to react to a message with a checkmark emoji.
Process: The `slack` skill adds a checkmark emoji as a reaction to the specified message.
Output: The message now has a checkmark emoji as a reaction.
```

## Error Handling

| Error Scenario | Reason | Resolution |
|:---------------|:-------|:-----------|
| Configuration error | Missing or incorrectly formatted parameters | Check the dependency requirements and configuration instructions. |
| Runtime error | Incompatible runtime environment | Confirm that the runtime environment meets the requirements. |
| Network error | Connection timeout or unreachability | Check the network connection and try again. Consider alternative domestic solutions if necessary. |

## Common Questions

### Q1: How do I start using Slack?

A: Please refer to the usage process section to ensure that the environment meets the dependency requirements.

### Q2: What should I do if I encounter an error?

A: Refer to the error handling section for instructions on how to resolve common issues.

### Q3: What are the limitations of Slack?

A: Refer to the known limitations section for information about the skill's capabilities and restrictions.

## Known Limitations

- Requires LLM support, which is not available without an LLM environment.
- Complex scenarios may require human judgment.
- Performance depends on the underlying model capabilities.

## Conclusion

The `slack` skill offers a robust set of functionalities to enhance team communication and streamline workflows through SkillHub. By providing detailed documentation and actionable examples, this skill empowers users to automate Slack interactions efficiently and effectively.

## 依赖说明

- LLM/API Key: 需要配置相应的API密钥
- 网络连接: 需要访问外部服务
- 文件系统: 需要读写文件权限
