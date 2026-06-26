## Description: <br>
用于快手数据分析、快手热榜、快手作品研究、关键词观察、内容调研、竞品分析和趋势研究，覆盖 Kuaishou / Kwai hot list and work research，来自 SocialDataX 社媒数据助手。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research Kuaishou hot-search trends, keyword results, short-video works, competitor content, and related social media signals through SocialDataX. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is labeled for Kuaishou but also documents Weibo and WeChat Channels research commands. <br>
Mitigation: Confirm the intended platform before use and keep Kuaishou hot-list or search results separate from Weibo and WeChat Channels outputs. <br>
Risk: The skill requires SOCIALDATAX_API_KEY and invokes the socialdatax-skills npm package through npx. <br>
Mitigation: Provide the API key only when intending to use SocialDataX, and review the npm package trust before installation or execution. <br>
Risk: Search pagination uses opaque next-page tokens that can be invalidated if edited. <br>
Mitigation: Pass returned pagination tokens back unchanged within the same search chain and stop only when no next-page token is returned. <br>


## Reference(s): <br>
- [SocialDataX API access homepage](https://socialdatax.52choujiang.com/?from=clawhub) <br>
- [ClawHub skill page](https://clawhub.ai/devinchen2014/socialdatax-kuaishou-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include content IDs, URLs, titles, author facts, interaction counts, publish times, pagination markers, and separate observed evidence from interpretation.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
