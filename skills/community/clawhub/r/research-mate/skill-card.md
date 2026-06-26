## Description: <br>
ResearchMate helps agents collect, verify, score, and package public-source materials for long-form articles, reports, and video scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yitao2027](https://clawhub.ai/user/yitao2027) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, analysts, researchers, and content teams use this skill to gather public source material for business, technology, finance, policy, academic, event, and international topics before drafting long-form work. It guides the agent through topic clarification, source routing, anti-hallucination checks, quality scoring, and structured source-pack creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics and keywords may be sent to public web search and saved in generated workspace files. <br>
Mitigation: Use non-confidential topics unless the user is comfortable with those keywords being searched and the resulting files remaining in the workspace. <br>
Risk: Collected source material may still be stale, incomplete, or unsuitable for publication even after automated checks. <br>
Mitigation: Review source URLs, publication dates, verification labels, and quality scores before citing or publishing any material. <br>
Risk: The README describes a separate GitHub/Python command-line project that is outside the scanned Skill files. <br>
Mitigation: Review that project, its dependencies, and its install path separately before using the command-line workflow. <br>


## Reference(s): <br>
- [ResearchMate on ClawHub](https://clawhub.ai/yitao2027/research-mate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, CSV, Files, Guidance] <br>
**Output Format:** [Markdown source pack with a CSV evaluation table and structured citation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create workspace files containing collected public-source material, source URLs, timestamps, verification notes, quality scores, and adoption guidance.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
