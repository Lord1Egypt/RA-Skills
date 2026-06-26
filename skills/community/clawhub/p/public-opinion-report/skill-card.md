## Description: <br>
Calls the Midu Public Opinion Report service to generate public opinion analysis reports, including incident, topic, industry, event, periodic, brand insight, city benchmarking, regional network information, and public policy online opinion reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bitallin](https://clawhub.ai/user/bitallin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request Markdown-format public opinion analysis reports from the Midu report service. It supports report-generation requests for events, topics, industries, activities, brands, cities, regions, and public policy monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and an API key to a hardcoded Midu HTTP endpoint. <br>
Mitigation: Install only when the Midu internal host and network path are trusted, and avoid sending sensitive content. <br>
Risk: API key exposure could occur if credentials are pasted into chats, reports, or shared files. <br>
Mitigation: Set MIDU_API_KEY through protected environment or OpenClaw configuration mechanisms instead of including the key in prompts or generated content. <br>


## Reference(s): <br>
- [Midu API Key Setup Guide](references/apikey-fetch.md) <br>
- [Public Opinion Report Skill Page](https://clawhub.ai/bitallin/public-opinion-report) <br>
- [Midu API Key Endpoint](http://intra-znjs-yqt-agent-wx-beta.midu.cc/apiKey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON response containing a Markdown report result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and MIDU_API_KEY; report generation may take 5 to 20 minutes.] <br>

## Skill Version(s): <br>
0.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
