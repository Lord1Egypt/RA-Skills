## Description: <br>
Generate RedNote image series with structured style and layout choices and bundled generation tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[632657122](https://clawhub.ai/user/632657122) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and agents use this skill to plan and generate connected RedNote card series, cover cards, and social infographic sequences from a topic or outline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local reference-image paths may be read from disk and uploaded to WeryAI even though the skill text says local paths are rejected. <br>
Mitigation: Before generation, review prompt and batch files for local paths and use only intended image files or public reference URLs. <br>
Risk: The image generation API key may be persisted in a local .image-skills/rednote-images/.env file. <br>
Mitigation: Keep the local .env file out of version control and treat IMAGE_GEN_API_KEY as a runtime secret. <br>
Risk: The skill sends prompts and image references to the WeryAI gateway. <br>
Mitigation: Avoid using sensitive prompts or reference images unless the workspace and WeryAI use are approved for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/632657122/rednote-images) <br>
- [RedNote dimensions reference](references/dimensions.md) <br>
- [RedNote prompt template](references/prompt-template.md) <br>
- [RedNote presets](references/presets.md) <br>
- [WeryAI text-to-image API documentation](https://docs.weryai.com/api-reference/image-generation/submit-text-to-image-task) <br>
- [WeryAI image-to-image API documentation](https://docs.weryai.com/api-reference/image-generation/submit-image-to-image-task) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Files, API calls] <br>
**Output Format:** [Markdown instructions with bash commands, generated prompt files, batch JSON, and image outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMAGE_GEN_API_KEY and Node.js/npm; uses bun or npx for TypeScript helper scripts.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
