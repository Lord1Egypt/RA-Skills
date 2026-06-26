## Description: <br>
Search X (Twitter) posts using the xAI API for tweets, social posts, and current discussion about a topic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevinbrother](https://clawhub.ai/user/kevinbrother) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search X posts through xAI, filter by handles or dates, and return readable results with citations to original posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and filters are sent to xAI for processing. <br>
Mitigation: Avoid secrets, private investigations, and sensitive internal topics unless that external processing is acceptable. <br>
Risk: The skill requires an xAI API key. <br>
Mitigation: Provide the key through XAI_API_KEY or approved agent configuration, and do not paste credentials into prompts or shared output. <br>


## Reference(s): <br>
- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search) <br>
- [xAI Console](https://console.x.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, citations, guidance] <br>
**Output Format:** [JSON containing status, query, result text, citations, search count, and token usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports handle filters, handle exclusions, date ranges, and optional image or video understanding.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
