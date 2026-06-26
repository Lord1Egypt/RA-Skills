## Description: <br>
按频道与日期查电视节目单，可查频道列表。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to list supported TV channels and retrieve a channel's program schedule for a specified date. It supports answers to TV-program questions such as what is airing tonight on CCTV or Hunan TV. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured JisuAPI app key and TV query parameters are sent to api.jisuapi.com. <br>
Mitigation: Install only when this third-party API use is acceptable, and scope, rotate, and revoke the JISU_API_KEY according to local credential policy. <br>
Risk: TV schedule lookups can fail because of missing parameters, invalid channel IDs, quota limits, expired keys, or API maintenance. <br>
Mitigation: Handle the skill's structured error responses before presenting results, and ask the user for a valid channel or date when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/tv) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jisuapi) <br>
- [JisuAPI TV Program API](https://www.jisuapi.com/api/tv/) <br>
- [JisuAPI home](https://www.jisuapi.com/) <br>
- [JisuAPI TV endpoint](https://api.jisuapi.com/tv) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON from the TV API, often summarized as text or Markdown for the user] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; query calls require tvid and a YYYY-MM-DD date.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
