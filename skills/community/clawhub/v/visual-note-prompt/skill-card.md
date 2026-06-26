## Description: <br>
将简短文本转换为知识卡片图片的提示词生成器（社区精简版）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spiderzhcl](https://clawhub.ai/user/spiderzhcl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn short Chinese study notes, concept summaries, or bullet points into structured visual-note image prompts for knowledge-card generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated prompts enforce fixed Chinese formatting and creator attribution, which may not match every user's intended style or language. <br>
Mitigation: Review generated prompt blocks before sending them to an image model, especially the displayed text, attribution, and negative prompt requirements. <br>
Risk: The packaged release does not include server-resolved GitHub provenance for this version. <br>
Mitigation: Use the packaged artifact as the reviewed source of truth, and independently verify any external repository before installing from a README clone command. <br>


## Reference(s): <br>
- [Format Guide](references/format-guide.md) <br>
- [Style Library](assets/style-library.md) <br>
- [ClawHub skill page](https://clawhub.ai/spiderzhcl/visual-note-prompt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style structured image prompt blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one or more 3:4 visual-note prompt blocks with fixed fields, negative prompts, and creator attribution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
