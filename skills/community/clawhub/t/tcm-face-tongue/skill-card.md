## Description: <br>
中医面舌辨证。调用 RageHealth 开放接口，对人脸 / 舌头图片做中医辨证。包含「望面」(`face-tcm-analyse`)、「望舌」(`tongue-diagnosis`)、「面舌辨证」(`comprehensive-interpretation`) 三个子接口，输出体质（平和/气虚/阳虚/阴虚/痰湿/湿热/血瘀/气郁/特禀/气阴两虚）、五脏（心肝脾肺肾）阴阳得分、症状、面色/舌象分类、推荐食谱、综合解读等。当用户上传人脸/舌头照片要求"中医辨证"、"看体质"、"望面望舌"、"面诊舌诊"、"五脏分析"时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qianchen94](https://clawhub.ai/user/qianchen94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to call RageHealth face, tongue, or combined face-and-tongue analysis APIs and turn the returned JSON into concise traditional Chinese medicine body-constitution, organ-balance, tongue-image, recipe, and care guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends face or tongue photos, optional demographic or location details, and RageHealth API credentials to a configured external RageHealth endpoint. <br>
Mitigation: Confirm user consent, send only needed inputs, verify the intended base URL before use, and protect TCM_AK and TCM_SK as secrets. <br>
Risk: Face ID detection can involve additional face-feature data handling. <br>
Mitigation: Enable faceIdDetect only when explicitly needed and authorized, and require a userGroup when it is enabled. <br>
Risk: The skill produces traditional Chinese medicine interpretations and recipe suggestions that could be mistaken for clinical advice. <br>
Mitigation: Present results as reference-only wellness guidance, advise professional medical care for serious or persistent symptoms, and flag special populations or medication users to follow clinician advice. <br>
Risk: Runtime dependencies are specified as minimum versions rather than a reviewed lockfile. <br>
Mitigation: Use pinned dependencies or a reviewed lockfile in sensitive environments. <br>


## Reference(s): <br>
- [tcm-face-tongue ClawHub Skill Page](https://clawhub.ai/qianchen94/skills/tcm-face-tongue) <br>
- [Response Schema](artifact/references/response_schema.md) <br>
- [RageHealth Credential Registration](https://ragehealth.cn/client) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write full API responses to JSON files; terminal output removes large landmark and polygon arrays unless full output is requested.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
