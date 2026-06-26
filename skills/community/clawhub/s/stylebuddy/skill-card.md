## Description: <br>
StyleBuddy is an OpenClaw wardrobe assistant that records clothing from photos or text, recommends outfits for weather and occasions, offers shopping advice, and analyzes wardrobe gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[89kpjddmtb-ui](https://clawhub.ai/user/89kpjddmtb-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use StyleBuddy to manage a personal wardrobe, get outfit recommendations, evaluate prospective clothing purchases, and receive wardrobe analysis. The skill is aimed at everyday style planning rather than software development workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores wardrobe records, outfit history, preferences, backups, and saved images locally. <br>
Mitigation: Avoid adding photos with sensitive background details and review local saved images and backups periodically. <br>
Risk: The skill may contact a weather service for outfit recommendations. <br>
Mitigation: Disable weather integration or avoid sharing location-sensitive context if weather-based recommendations are not needed. <br>
Risk: Optional image-search or image-generation providers may receive data if users enable those API keys. <br>
Mitigation: Keep optional provider API keys disabled unless the user trusts the selected providers and their data handling. <br>


## Reference(s): <br>
- [StyleBuddy ClawHub page](https://clawhub.ai/89kpjddmtb-ui/stylebuddy) <br>
- [StyleBuddy feature design document](https://feishu.cn/docx/KRdZdGqScopSdUxF7rHcAUyPn2f) <br>
- [Open-Meteo forecast endpoint](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration, files] <br>
**Output Format:** [Markdown-style conversational text, optional image paths, and local backup data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include outfit recommendations, wardrobe summaries, shopping advice, analysis reports, and references to locally stored images or backups.] <br>

## Skill Version(s): <br>
0.4.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
