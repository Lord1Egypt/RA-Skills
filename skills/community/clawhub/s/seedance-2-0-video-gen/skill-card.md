## Description: <br>
Generate Seedance 2.0 videos through WeryAI for text-to-video, image-to-video, multi-image video, and first-frame/last-frame transitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[632657122](https://clawhub.ai/user/632657122) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and creative operators use this skill to prepare, confirm, and run WeryAI Seedance 2.0 video generations from text prompts or public HTTPS reference images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and public reference image URLs are sent to WeryAI for video generation. <br>
Mitigation: Use the skill only when WeryAI is trusted for the submitted content, and avoid sensitive prompts or private media URLs. <br>
Risk: Real wait or submit-* commands can spend WeryAI account credits. <br>
Mitigation: Use dry-run validation and the documented confirmation step before paid generation commands. <br>
Risk: The WERYAI_API_KEY secret could be exposed if written into files or shared transcripts. <br>
Mitigation: Keep WERYAI_API_KEY in the runtime environment and avoid storing the key in skill files or prompts. <br>
Risk: Optional WeryAI endpoint overrides can redirect requests away from the default API hosts. <br>
Mitigation: Set WERYAI_BASE_URL or WERYAI_MODELS_BASE_URL only for trusted environments. <br>


## Reference(s): <br>
- [Seedance 2.0 Prompt Optimization](references/seedance-prompt-optimization.md) <br>
- [ClawHub release page](https://clawhub.ai/632657122/seedance-2-0-video-gen) <br>
- [WeryAI API key setup](https://www.weryai.com/api/keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON task results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include expanded prompts, confirmation tables, WeryAI task IDs, task status, and video URLs; real wait and submit-* commands require WERYAI_API_KEY and may spend account credits.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
