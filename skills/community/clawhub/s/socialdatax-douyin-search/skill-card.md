## Description: <br>
Helps agents retrieve and summarize Douyin hot-search and keyword search results for content research, competitor analysis, and trend scanning through SocialDataX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, marketers, and developers use this skill to inspect Douyin hot-search rankings and search public Douyin works for content research, trend monitoring, and competitor analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server security guidance cautions that the skill may run CLI commands and may read deployment performance insights, including production insights if directed. <br>
Mitigation: Install only when that access is intended, prefer pinned or already installed CLI tools when supply-chain control matters, and scope production access deliberately. <br>
Risk: The direct CLI examples use npx to run the socialdatax-skills package. <br>
Mitigation: Use a pinned or preinstalled package version when supply-chain control matters. <br>
Risk: The skill requires SOCIALDATAX_API_KEY for data calls. <br>
Mitigation: Provide the key through environment variables only and avoid storing it in prompts, files, or shared logs. <br>
Risk: Search results and hot-search rankings are external data and may change over time. <br>
Mitigation: Keep observed facts separate from interpretation and include returned identifiers, URLs, timestamps, and counts when traceability matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/devinchen2014/socialdatax-douyin-search) <br>
- [SocialDataX API Access Homepage](https://socialdatax.52choujiang.com/?from=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOCIALDATAX_API_KEY plus node and npm; search pagination uses returned next_page_token values unchanged.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
