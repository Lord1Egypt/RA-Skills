## Description:

洒洒（房车陪伴助手）。会说话的德牧导航官，净如姐房车旅途的小狗搭子。唤醒口令「洒洒，洒洒」，可语音控制高德导航、邮件回复、百度/谷歌搜索、腾讯会议及常用App。

This skill is for demonstration purposes and not for production usage.

## Publisher:

[clara-wang-2023](https://clawhub.ai/user/clara-wang-2023)

### License/Terms of Use:

MIT-0

## Use Case:

External RV travelers and skill evaluators can use this static browser skill to interact with a Chinese text and voice companion persona for RV travel prompts such as navigation-style requests, traffic, fuel stations, email, meetings, search, and camera actions. Treat it as a simulated assistant rather than a source of real driving, traffic, email, meeting, search, or camera actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents navigation, traffic, fuel, email, meeting, search, and camera actions as completed even though the artifact is a static browser prototype.

Mitigation: Label these capabilities as simulations and require verified integrations before relying on them for travel, communication, search, or camera workflows.

Risk: Users may enter sensitive text or speech into a page with unsafe HTML rendering and browser speech recognition.

Mitigation: Avoid sensitive inputs unless rendering is sanitized and users understand that browser or vendor speech services may process audio.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clara-wang-2023/skills/sasa)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Chinese conversational responses in a browser chat interface]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are scripted and simulated; supported browsers may also accept speech recognition input.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
