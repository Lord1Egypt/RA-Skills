## Description: <br>
Generates precise, timecoded Seedance 2.0 prompts that map multimodal assets to controlled short-form video generation and editing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dandysuper](https://clawhub.ai/user/dandysuper) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and prompt engineers use this skill to turn rough video ideas and reference media into Seedance 2.0 prompts with explicit modes, asset mappings, timeline beats, negative constraints, and generation settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional shell helpers create local files and directories when run. <br>
Mitigation: Review helper scripts before running them and execute them only in a dedicated workspace directory. <br>
Risk: Prompts and media later uploaded to external video-generation services may be shared with that provider. <br>
Mitigation: Avoid uploading sensitive media or confidential prompts unless the target service terms and data-handling practices are acceptable. <br>
Risk: Seedance prompts may be rejected when they include recognizable franchise, character, brand, or realistic face references. <br>
Mitigation: Use original names, generic visual descriptions, explicit negative constraints, and IP-safe prompt variants as described by the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dandysuper/seedance-2-prompt-engineering-skill) <br>
- [Seedance 2.0 Prompt Recipes](artifact/references/recipes.md) <br>
- [Modes and Interaction Notes](artifact/references/modes-and-recipes.md) <br>
- [Camera Language & Visual Styles Vocabulary](artifact/references/camera-and-styles.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown prompt structures with optional inline shell commands for local workspace setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Seedance mode selection, asset mapping, timecoded prompt beats, negative constraints, and generation settings.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
