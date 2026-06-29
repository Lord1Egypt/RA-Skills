## Description: <br>
根据目的地实时天气、行程天数、出行类型和旅行者构成，智能生成个性化打包清单，支持打包进度检查和出行贴士提醒。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to create destination-aware packing checklists, review packing progress, and receive concise trip preparation tips based on trip length, travel style, destination scene, traveler composition, and optional weather lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Destination city queries may be sent to a third-party Gaode proxy during weather-aware list generation. <br>
Mitigation: Install only if that data flow is acceptable, and use quick mode when local-only packing suggestions are sufficient. <br>
Risk: The artifact claims all data is local and no external requests are sent, but the security evidence reports a hardcoded external weather proxy. <br>
Mitigation: Treat the local-only privacy statement as unreliable until the publisher corrects the documentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/smart-packing-list) <br>
- [Publisher profile](https://clawhub.ai/user/travel-skills) <br>
- [Gaode weather proxy endpoint](https://gaode-proxy-jerspxcked.cn-hangzhou.fcapp.run) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [Structured JSON responses containing Chinese text for weather summaries, categorized packing checklists, packing progress, alerts, and travel tips.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generate command depends on a third-party Gaode proxy for weather lookup; quick and check modes use local checklist logic.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
