## Description: <br>
生成 Zao Live 分享卡片，当用户想要收听早播、新闻或播客音频时返回可点击的分享链接。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Emotibot5](https://clawhub.ai/user/Emotibot5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-language chat agents and users use this skill to turn news, podcast, or Zao Live listening requests into a shareable Zao Live morning-news audio link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may route generic news or podcast requests to Zao Live. <br>
Mitigation: Narrow trigger wording before deployment if the agent should only respond to Zao-specific requests. <br>
Risk: Opening generated Zao Live links may share normal visit data with the platform. <br>
Mitigation: Tell users that external link visits are governed by Zao Live's terms and privacy practices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Emotibot5/zaobo-news) <br>
- [Zao Live homepage](https://zao.live) <br>
- [Zao Live new share endpoint](https://zao.live/zaobo/newshare) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, guidance] <br>
**Output Format:** [Markdown link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a concise clickable Zao Live share link; generated links may expire and platform visits may be logged by Zao Live.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
