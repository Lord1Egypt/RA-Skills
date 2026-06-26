## Description: <br>
Use when the user needs WeryAI image tools to analyze and transform existing images. Generate reusable prompts, convert and optimize visuals via background removal/change, canvas expansion, face swap, reframe, repair, text erase, translation, and upscale workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weryai-developer](https://clawhub.ai/user/weryai-developer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to route existing-image editing requests to WeryAI tools for prompt extraction, background editing, canvas expansion, face swap, reframing, repair, text erasure, translation, and upscaling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local paths supplied as image fields can be uploaded to WeryAI. <br>
Mitigation: Prefer explicit HTTPS image URLs, avoid sensitive local paths, and run dry-run previews before paid processing. <br>
Risk: Real submit and wait commands can consume WeryAI credits. <br>
Mitigation: Confirm ambiguous or expensive requests before running paid jobs and use dry-run validation when checking request shape. <br>
Risk: The optional WERYAI_BASE_URL override can direct requests to a different host. <br>
Mitigation: Leave the default API host in place unless the alternate endpoint is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weryai-developer/weryai-image-toolkits) <br>
- [WeryAI Image Tools Matrix](references/image-tools-matrix.md) <br>
- [WeryAI documentation index](https://docs.weryai.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, text] <br>
**Output Format:** [Markdown with command examples and JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return image URLs, prompt text, task identifiers, task status, cost metadata, and request summaries from WeryAI responses.] <br>

## Skill Version(s): <br>
0.1.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
