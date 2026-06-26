## Description: <br>
Searches shopping platforms such as Taobao, JD, Pinduoduo, and Amazon and formats results with the user's configured affiliate identifiers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mi426878](https://clawhub.ai/user/mi426878) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure affiliate identifiers, search supported shopping platforms, compare displayed offers, and produce affiliate sharing links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake generated product titles, prices, sales counts, discounts, or commission estimates for verified shopping data. <br>
Mitigation: Label these fields as unverified unless the skill is changed to call verified provider APIs and validate returned data. <br>
Risk: Affiliate links may be generated during ordinary shopping requests without a clear commercial disclosure. <br>
Mitigation: Use the skill only when affiliate-link generation is intended and disclose the affiliate relationship before sharing generated links. <br>
Risk: Configured affiliate identifiers are stored locally and inserted into generated URLs. <br>
Mitigation: Review the local configuration before use and avoid storing identifiers in shared workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mi426878/shopping-affiliate-search) <br>
- [Publisher profile](https://clawhub.ai/user/mi426878) <br>
- [Alimama publisher portal](https://pub.alimama.com) <br>
- [JD Union](https://union.jd.com) <br>
- [Pinduoduo Jinbao](https://jinbao.pinduoduo.com) <br>
- [Amazon Associates](https://affiliate-program.amazon.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal text with product entries, prices, commission estimates, and affiliate URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes affiliate configuration to a local JSON file and prints search results to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
