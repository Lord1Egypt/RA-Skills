## Description: <br>
Generates YouMind-style illustrated PPT presentations from a user's outline, using a consistent cute IP character, visual-story structure, AI image prompts, and slide assembly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoliu166](https://clawhub.ai/user/xiaoliu166) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Presentation creators, teams, and developers use this skill to turn outlines into visual narrative decks for product launches, personal growth stories, project retrospectives, team reports, and brand storytelling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency installation steps may add npm or pip packages to the working environment. <br>
Mitigation: Run the skill in a project or temporary directory and review dependency installs before allowing them. <br>
Risk: User outlines may be sent to an external image-generation provider as part of prompt creation. <br>
Mitigation: Avoid confidential outline details unless the configured image provider is approved for that data. <br>
Risk: Generated slide text, visuals, or prompts may misrepresent the source outline. <br>
Mitigation: Review the staged narrative plan, visual plan, generated prompts, and final PPTX before sharing. <br>


## Reference(s): <br>
- [IP Role Presets](references/ip-presets.md) <br>
- [Prompt Templates](references/prompt-templates.md) <br>
- [Visual Logic Mapping Guide](references/visual-logic.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaoliu166/youmind-ppt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance, English image prompts, code snippets, shell commands, and PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses staged user confirmations before final rendering; may rely on external image generation and local PPTX tooling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
