## Description: <br>
查询城市限行规则与尾号，可查支持城市列表。当用户说：北京明天限行尾号是几？成都限行区域怎么算？或类似限行问题时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to check supported Chinese cities and retrieve vehicle license plate restriction times, areas, summaries, and restricted plate numbers for a specified city and date. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the configured JisuAPI key and queried city/date to JisuAPI. <br>
Mitigation: Use the skill only when that data sharing is acceptable, prefer a dedicated or limited API key when available, and rotate or revoke the key if exposure is suspected. <br>
Risk: API quota usage or access restrictions may affect availability. <br>
Mitigation: Monitor JisuAPI quota and error responses, and present returned API errors clearly to the user. <br>
Risk: The skill depends on the Python requests package. <br>
Mitigation: Install requests from a trusted package source and keep the runtime environment controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/vehiclelimit) <br>
- [JisuAPI Vehicle License Plate Restriction API](https://www.jisuapi.com/api/vehiclelimit/) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests Python package, and JISU_API_KEY; command output is JSON returned from JisuAPI or structured error JSON.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
