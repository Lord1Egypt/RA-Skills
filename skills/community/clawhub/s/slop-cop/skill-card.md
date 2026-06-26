## Description: <br>
Judges visual design assets and AI-generated images before they ship, including layout defects, hallucinated text, and semantic consistency between copy and visuals/data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chchchadzilla](https://clawhub.ai/user/chchchadzilla) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, founders, marketers, and design reviewers use this skill to audit image assets, UI screenshots, marketing creative, charts, and generated visual variants before release. It produces strict ship/fix/kill verdicts, concrete defects, and a recommendation for single-asset or comparative review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask an agent to inspect user-provided images through the OpenClaw image tool. <br>
Mitigation: Avoid using it on private or sensitive images unless that processing is acceptable in the deployment environment. <br>
Risk: Visual verdicts may affect whether creative assets are shipped, fixed, or rejected. <br>
Mitigation: Review the reported defects and recommendations before applying release decisions in production workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chchchadzilla/slop-cop) <br>
- [README](README.md) <br>
- [Vision Prompt Template](references/vision-prompt-template.md) <br>
- [Per-Asset Checklist](references/checklist.md) <br>
- [Anti-Patterns to Flag](references/anti-patterns.md) <br>
- [Semantic Consistency Checks](references/semantic-consistency.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured verdicts, defects, recommendations, and deploy notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Verdicts use SHIP, FIX, or KILL; comparative mode may rank candidates and recommend one asset.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
