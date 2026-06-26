## Description: <br>
减肥进度追踪助手。用户告诉 AI 今天的体重，AI 自动帮您记录并生成漂亮的图表，清晰展示减肥进度。支持中英文界面，macOS/Windows/Linux 多平台使用。当用户说"记录体重"、"今天体重"、"减肥打卡"、"体重多少"时自动触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mixinan](https://clawhub.ai/user/mixinan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to record daily body weight, maintain local JSON history, and view progress toward a weight goal in a browser-based chart. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weight history and goals are personal data stored in local JSON files. <br>
Mitigation: Keep the skill folder private and install only if local storage of this data is acceptable. <br>
Risk: Serving the tracker beyond localhost can expose personal weight data on a local network. <br>
Mitigation: Prefer localhost-only viewing and avoid LAN sharing unless the exposure is understood and intended. <br>
Risk: Port-based process cleanup commands can stop the wrong process if used carelessly. <br>
Mitigation: Verify the exact server process before running any kill command. <br>
Risk: The setup script changes local configuration and data files. <br>
Mitigation: Run setup.sh without administrator privileges and review generated config.json and weight_history.json after setup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mixinan/weight-tracker) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mixinan) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [User guide](artifact/assets/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and local JSON updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local configuration and weight-history JSON files; browser visualization is served from local files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
