## Description: <br>
Design production English prompts for Seedance 2.0 then generate text-to-video or image-to-video on WeryAI (`SEEDANCE_2_0`), using bundled recipes (A-K), mode-to-JSON mapping, camera vocabulary, and pre-flight checklists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to turn short video briefs or image references into structured Seedance 2.0 prompts and WeryAI JSON submissions. It supports text-to-video, single-image, multi-image, and first/last-frame workflows after explicit pre-submit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid WeryAI generation calls can consume credits, including retries or blocking wait calls. <br>
Mitigation: Require explicit approval of the full prompt, model, duration, aspect ratio, resolution, audio setting, and reference URLs before any submit or wait command. <br>
Risk: A WERYAI_API_KEY is required for model lookup, generation, status checks, and local image upload. <br>
Mitigation: Treat the API key as a secret, keep it in the environment, and never write it into prompts, skill files, logs, or generated artifacts. <br>
Risk: Local image paths may be read and uploaded to WeryAI when used for image-to-video flows. <br>
Mitigation: Prefer public HTTPS image URLs; use local paths only after reviewing upload behavior and obtaining explicit consent to read and upload the file. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zoucdr/seedance-2-prompt-engineering-to-video) <br>
- [WeryAI Video CLI and JSON](artifact/resources/WERYAI_VIDEO_API.md) <br>
- [Seedance 2 Prompt Engineering Playbook](artifact/resources/seedance2-prompt-engineering-playbook.md) <br>
- [Modes and WeryAI Mapping](artifact/resources/modes-and-weryai-mapping.md) <br>
- [Recipes for WeryAI](artifact/resources/recipes-weryai.md) <br>
- [Camera and Styles](artifact/resources/camera-and-styles.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with parameter tables, inline links, JSON payloads, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce WeryAI task identifiers and playable video links after explicit user confirmation.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata; artifact frontmatter is 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
