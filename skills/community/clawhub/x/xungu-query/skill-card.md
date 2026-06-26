## Description: <br>
A Chinese divination assistant for BaZi, daily fortune, Liu Yao, Da Liu Ren, Lu Ming, and luck-cycle readings using xungufa.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnyouker](https://clawhub.ai/user/cnyouker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users ask an agent for Chinese divination outputs, including BaZi charts, daily fortunes, Liu Yao casts, Da Liu Ren charts, Lu Ming readings, and annual luck-cycle analysis. The skill helps collect the needed birth or casting details, call the provider service, and present formatted results for user review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Birth details, casting times, and optionally an API token may be shared with xungufa.com. <br>
Mitigation: Use the skill only when that data sharing is acceptable, and avoid entering information that should not be sent to the provider. <br>
Risk: Local birth profiles can persist across future sessions if saved. <br>
Mitigation: Save a profile only after explicit consent and delete it when reuse is no longer wanted. <br>
Risk: API responses or divination outputs may include content that should not be treated as authoritative advice. <br>
Mitigation: Treat results as interpretive guidance and review outputs before relying on them for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnyouker/xungu-query) <br>
- [Publisher profile](https://clawhub.ai/user/cnyouker) <br>
- [xungufa.com](https://xungufa.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown text with formatted divination tables, API examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require an XUNGU_API_TOKEN for Liu Yao, Da Liu Ren, and full-feature access.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
