## Description: <br>
Reverse-engineers AI video prompts from videos, screenshots, or descriptions by analyzing cinematography, visual style, model fit, and reproduction workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chang9852](https://clawhub.ai/user/chang9852) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, editors, and developers use this skill to deconstruct a video's visual language and generate structured prompts for AI video tools. It supports shot-by-shot analysis, global style prompts, model estimates, parameter guidance, and a reproduction workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input media or links may contain sensitive or private visual content. <br>
Mitigation: Only provide media that is appropriate to have analyzed, and review generated descriptions before sharing them. <br>
Risk: HappyHorse-specific guidance may favor Chinese prompts when optimizing for that model. <br>
Mitigation: Specify the desired output language when requesting prompts if Chinese output is not wanted. <br>


## Reference(s): <br>
- [Video AI Models & Cinematography Reference](references/model_params.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with structured prompt blocks and parameter tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes shot breakdowns, model estimates, global prompts, negative prompts, and workflow guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
