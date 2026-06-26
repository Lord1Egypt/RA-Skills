## Description: <br>
Verifies Chinese GitHub developers by correlating public profile evidence across Bilibili, Douyin, Xiaohongshu, Zhihu, Juejin, and CSDN. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuchenggong19851114-design](https://clawhub.ai/user/zhuchenggong19851114-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users evaluating GitHub projects can ask an agent to search public Chinese social and developer platforms for an author's presence and summarize identity-correlation signals. Results should be treated as limited public-profile clues rather than a trust score, hiring judgment, or safety verdict. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can turn weak public-profile correlation into overconfident trust judgments. <br>
Mitigation: Frame results as limited identity-matching clues, not trust scores, hiring judgments, or safety verdicts. <br>
Risk: Absence from the listed regional social platforms could be misread as negative evidence. <br>
Mitigation: Avoid penalizing missing social-platform presence and state when evidence is unavailable or inconclusive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuchenggong19851114-design/zhuchenggong-github-source-verification) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summary with a verification table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public profile links, follower or content counts, and a credibility note.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
