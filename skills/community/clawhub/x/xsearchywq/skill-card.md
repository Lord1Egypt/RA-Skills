## Description: <br>
Search X (Twitter) posts using the xAI API when a user wants to find tweets, look up what people are saying on X, or find social media posts about a topic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ywqsimmon](https://clawhub.ai/user/ywqsimmon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search recent X/Twitter posts through xAI, optionally filtering by handle, excluding handles, setting date ranges, and enabling media understanding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an xAI API key and sends user search queries to xAI. <br>
Mitigation: Install only if the user is comfortable providing XAI_API_KEY and sending search queries to xAI; review xAI account billing and data handling expectations before use. <br>
Risk: Search results and citations depend on xAI's X search behavior and may reflect incomplete, changing, or summarized social media content. <br>
Mitigation: Review cited original X posts before relying on results for important decisions or publication. <br>


## Reference(s): <br>
- [xAI x-search documentation](https://docs.x.ai/developers/tools/x-search) <br>
- [xAI console](https://console.x.ai) <br>
- [ClawHub skill page](https://clawhub.ai/ywqsimmon/xsearchywq) <br>
- [Publisher profile](https://clawhub.ai/user/ywqsimmon) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and command-line output with citations to original X posts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and XAI_API_KEY; supports handle filters, excluded handles, date ranges, image understanding, and video understanding.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
