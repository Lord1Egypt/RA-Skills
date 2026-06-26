## Description: <br>
Guides users through structured Chinese-language questions and defaults to turn vague video ideas into professional 120-150 word English AI video generation prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[showtimewalker](https://clawhub.ai/user/showtimewalker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to refine simple or incomplete video concepts into generation-ready prompts for AI video tools. It provides a scene summary, decision table, English prompt, and concrete refinement directions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording may route general video or scene-description requests into this prompt-crafting workflow. <br>
Mitigation: Review whether the Chinese-guided video prompt workflow is desired for broad video ideation requests before deployment. <br>
Risk: The skill's default output format uses Chinese explanation around an English video prompt. <br>
Mitigation: Set a deployment or user instruction to use another surrounding language when Chinese-first guidance is not appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/showtimewalker/video-prompt-craft) <br>
- [Cinematography reference](reference/cinematography.md) <br>
- [Lighting and mood reference](reference/lighting_mood.md) <br>
- [Narrative techniques reference](reference/narrative_techniques.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with a Chinese scene summary, a decision table, a 120-150 word English video prompt, and refinement suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external API calls; surrounding explanation is Chinese-first unless the user overrides it.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
