## Description: <br>
Generates and edits images through VVMAI's OpenAI-compatible Images API, with nano-banana and gpt-image model support and optional local saving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leevigoo](https://clawhub.ai/user/leevigoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create or edit images from prompts, model choices, aspect ratios, image counts, and optional source images through a configured VVMAI account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, API keys, and any input images selected for editing are sent to the configured VVMAI API endpoint. <br>
Mitigation: Install only when you trust VVMAI and the configured VVMAI_BASE_URL, and avoid sensitive prompts or images unless that data sharing is acceptable. <br>
Risk: Some modes save generated image files locally, including gpt-image models and explicit save or OSS options. <br>
Mitigation: Review save flags and output directories before use, and handle generated files according to local data retention and sharing policies. <br>


## Reference(s): <br>
- [VVMAI API](https://api.vvmai.com) <br>
- [VVMAI API v1 Base URL](https://api.vvmai.com/v1) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/leevigoo/vvmai-image-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples and MEDIA output references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, VVMAI_API_KEY, and VVMAI_BASE_URL; generated images may be returned as URLs or saved as local files depending on model and flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
