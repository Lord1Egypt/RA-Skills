## Description: <br>
Parse anime storyboard scripts and generate four types of prompts: character prompts, scene prompts, Sora video generation prompts, and standard storyboard prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, storyboard artists, and prompt writers use this skill to turn anime storyboard notes into bilingual character, scene, Sora video, and standard storyboard prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated bilingual prompt output may not fit workflows that require one language or strict machine-parseable responses. <br>
Mitigation: Review and normalize the generated format before using it in automated image or video pipelines. <br>
Risk: Template-based visual style and quality keywords may be inconsistent with a project's preferred style guide. <br>
Mitigation: Review style keywords and keep a project-specific vocabulary before generation. <br>


## Reference(s): <br>
- [Prompt Template Library](references/templates.md) <br>
- [Storyboard Terminology Reference](references/terminology.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with bilingual prompt blocks and optional negative prompt sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include aspect ratio suggestions and batch entries for multiple storyboard panels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
