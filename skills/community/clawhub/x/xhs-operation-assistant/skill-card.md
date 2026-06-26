## Description: <br>
Helps content operators retrieve Xiaohongshu official-account notes and hot topics, and evaluate Xiaohongshu accounts and notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zfeng1982](https://clawhub.ai/user/zfeng1982) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and social media operators use this skill to look up Xiaohongshu official-account notes, review hot topics, and obtain scoring guidance for account profiles and note content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger terms could cause the skill to activate when the user only mentions Xiaohongshu topics. <br>
Mitigation: Invoke it for explicit Xiaohongshu operations requests and confirm intent before querying external data. <br>
Risk: Queries are sent to qianhaistonepark.site and may include account or note content. <br>
Mitigation: Avoid sharing sensitive private account or note content unless the user trusts the external service. <br>
Risk: API results may be empty, unavailable, or encoded. <br>
Mitigation: Report empty or failed API responses as unavailable and decode supported fields before presentation instead of inventing data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zfeng1982/xhs-operation-assistant) <br>
- [Project homepage](https://github.com/zfeng1982/xhs-operation-assistant) <br>
- [Xiaohongshu helper API base URL](https://qianhaistonepark.site/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with API response summaries, scoring guidance, and optional curl command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some returned fields may need decoding with the bundled helper before presentation.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
