## Description: <br>
Provides a Chinese-language A-share market commentary persona that responds in a Xu Zhuoxun-style first-person voice using investing models, trading heuristics, case studies, and trading psychology references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thinkpeace](https://clawhub.ai/user/thinkpeace) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to answer A-share market questions in Chinese with a named investing persona, including market analysis, position sizing, stop-loss discipline, fund-flow interpretation, trend judgment, and trading psychology. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce forceful A-share trading directions in a named persona. <br>
Mitigation: Treat outputs as educational commentary, require independent financial judgment, and avoid using responses as personalized investment advice. <br>
Risk: The skill may not repeat risk disclaimers after first activation. <br>
Mitigation: Surface a financial-risk disclaimer at deployment or session level and remind users that market decisions remain their responsibility. <br>
Risk: The skill roleplays a named private fund manager. <br>
Mitigation: Confirm the persona and source-rights posture before public deployment, and clearly label generated responses as AI-generated educational commentary. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thinkpeace/xuzhuoxun-perspective) <br>
- [Publisher Profile](https://clawhub.ai/user/thinkpeace) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Models Reference Set](artifact/references/models/) <br>
- [Heuristics Reference Set](artifact/references/heuristics/) <br>
- [Case Studies Reference Set](artifact/references/cases/) <br>
- [Trading Psychology](artifact/references/psychology/00-index.md) <br>
- [Expression Guidance](artifact/references/expression/00-index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown prose in Chinese, often with a conclusion, short reasons, cited mental model or heuristic, and action-oriented next steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include trading posture language such as buy, sell, hold, wait, stop-loss, and position-sizing guidance; the skill says it does not answer individual stock buy or sell recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
