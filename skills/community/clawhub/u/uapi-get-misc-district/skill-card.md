## Description: <br>
使用 UAPI 的“Adcode 国内外行政区域查询”单接口 skill，帮助 agent 准备并调用 GET /misc/district 查询行政区域信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when an agent needs to look up administrative regions by keyword, adcode, or coordinates through UAPI's GET /misc/district endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ambiguous requests that mention district could be routed to the UAPI Adcode lookup when the user intended a different meaning. <br>
Mitigation: Confirm that the user wants an administrative-region lookup before making an external call for broad or ambiguous district requests. <br>
Risk: Queries may include precise coordinates or sensitive location context. <br>
Mitigation: Ask for confirmation before sending precise location details to UAPI when the user's intent is unclear. <br>


## Reference(s): <br>
- [Quick Start](references/quick-start.md) <br>
- [Adcode 国内外行政区域查询](references/operations/get-misc-district.md) <br>
- [Misc 分类接口](references/resources/Misc.md) <br>
- [UAPI](https://uapis.cn) <br>
- [ClawHub Skill Page](https://clawhub.ai/shuakami/uapi-get-misc-district) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with endpoint, parameter, authentication, and response-code details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports keyword, adcode, and latitude/longitude query planning for the UAPI administrative-region lookup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
