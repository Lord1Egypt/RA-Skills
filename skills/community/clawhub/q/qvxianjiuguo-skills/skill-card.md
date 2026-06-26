## Description: <br>
机票模糊搜索技能，在用户查询机票或特价机票时，通过临近机场组合搜索来寻找更低价的航班方案。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[xiaoyiyebuaijianghua](https://clawhub.ai/user/xiaoyiyebuaijianghua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users use this skill to search low-cost flight options by expanding origin and destination airport ranges, then review nearby-airport and ground-transport tradeoffs. The skill is documented for technical learning and research use, not for booking, payment, or commercial scraping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill launches and controls Chrome to query third-party travel sites. <br>
Mitigation: Install only when browser automation is acceptable, use the dedicated browser profile described by the skill, and verify results on official travel channels before acting. <br>
Risk: The skill stores travel-site login cookies on disk. <br>
Mitigation: Use a secondary travel account, avoid sensitive primary accounts, and delete ~/.qvxian and ~/.qvxianjiuguo when finished. <br>
Risk: Debug HTML capture may save page contents locally. <br>
Mitigation: Keep debug capture disabled unless local storage of page contents is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoyiyebuaijianghua/qvxianjiuguo-skills) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with CLI commands and summarized flight-search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include login guidance, nearby-airport options, price summaries, and ground-transport notes; search results are informational and should be verified on official travel channels.] <br>

## Skill Version(s): <br>
3.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
