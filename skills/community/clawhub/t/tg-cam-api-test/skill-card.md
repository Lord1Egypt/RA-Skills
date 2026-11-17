## Description:

探鸽摄像头 Skill 服务。用于查询当前 Skill 已绑定设备、查看当前画面、查询事件、查看事件图片、确认设备状态和电量。当用户要查看可操作设备、看某个摄像头当前截图、查询某天或某时段发生了什么、查看最近事件或事件图片、确认在线状态、查询电量时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyfinec](https://clawhub.ai/user/flyfinec)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect bound camera devices, retrieve current snapshots, review events and event images, and check device online status or battery level. It is suited for camera monitoring workflows where the user can provide the required camera service credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose private camera images from homes, workplaces, or other sensitive areas.

Mitigation: Review intended camera coverage before installation and use explicit camera-specific requests when asking for snapshots or event images.

Risk: Camera API credentials are stored in local configuration and could be exposed if file access is too broad.

Mitigation: Restrict access to the configuration file, do not echo the API key in chat, and rotate the API key if it is exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/flyfinec/skills/tg-cam-api-test)
- [Publisher Profile](https://clawhub.ai/user/flyfinec)
- [Webcam Skill API Base URL](https://skill-test.webcamapp.cc)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown summaries with optional JSON configuration snippets and camera image results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TIVS_CLI_ID and TIVS_API_KEY credentials for authenticated camera API access.]

## Skill Version(s):

0.0.3 (source: release evidence and X-Skill-Version header)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
