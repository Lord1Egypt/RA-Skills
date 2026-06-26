## Description: <br>
This skill translates CCTV XinWenLianBo (新闻联播) official language into plain Chinese that educated general audiences can understand. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ltryee](https://clawhub.ai/user/ltryee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to fetch, translate, explain, and summarize CCTV XinWenLianBo transcripts into plain Chinese while separating reported facts from interpretive policy-signal analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad shorthand trigger words can activate the skill when the user did not intend to analyze XinWenLianBo content. <br>
Mitigation: Invoke it with explicit terms such as “新闻联播” or “央视新闻联播”, matching the server-provided security guidance. <br>
Risk: Policy-signal analysis is interpretive and may be mistaken for confirmed official intent. <br>
Mitigation: Keep facts and interpretation clearly separated, preserve uncertainty labels, and base summaries on the public CCTV transcript text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ltryee/xinwenlianbo-translator) <br>
- [CCTV XinWenLianBo transcript index](https://tv.cctv.com/lm/xwlb/index.shtml) <br>
- [XinWenLianBo jargon dictionary](references/xinwenlianbo-jargon-dictionary.md) <br>
- [XinWenLianBo structure guide](references/xinwenlianbo-structure-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown in plain Chinese] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes plain-language explanations, key facts, impact notes, jargon translation tables, uncertainty labels, and daily signal summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
