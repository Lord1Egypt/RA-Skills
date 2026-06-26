## Description: <br>
Provides read-only Kuaishou/Kwai work detail lookups through SocialDataX for content details, interaction metrics, and content analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and content researchers use this skill to fetch a structured view of one Kuaishou/Kwai work by photo ID or URL for content research and interaction-metric review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a SocialDataX API key and invokes the external socialdatax-skills npm package to retrieve social media detail data. <br>
Mitigation: Use it only when SocialDataX and the npm package are trusted, and provide only the required SOCIALDATAX_API_KEY in the execution environment. <br>
Risk: Returned social media metrics and content details may be incomplete, unavailable, or unsuitable for unsupported account actions. <br>
Mitigation: Treat the skill as a read-only lookup helper and review returned factual fields before using them in analysis or downstream reports. <br>


## Reference(s): <br>
- [SocialDataX API Access](https://socialdatax.52choujiang.com/?from=clawhub) <br>
- [ClawHub Skill Page](https://clawhub.ai/devinchen2014/socialdatax-kuaishou-detail) <br>
- [Publisher Profile](https://clawhub.ai/user/devinchen2014) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON data returned by the SocialDataX CLI or MCP tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOCIALDATAX_API_KEY plus node and npm; lookup commands are read-only.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
