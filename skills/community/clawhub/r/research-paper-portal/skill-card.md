## Description: <br>
Creates personalized academic paper portal websites for researchers by collecting recent papers, generating AI background images, and publishing the site. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JiaxiLiao](https://clawhub.ai/user/JiaxiLiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and academic teams use this skill to configure a research-paper navigation site, collect papers from OpenAlex, arXiv, and RSS sources, generate paper artwork, and publish daily updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Externally fetched paper text can influence a local LLM shell command in the paper update workflow. <br>
Mitigation: Review and fix scripts/update-papers.py before running or scheduling it by replacing shell=True string execution with argument-list execution or a provider SDK, and restrict the LLM command to an allowlisted tool. <br>
Risk: Automatic publishing can move generated paper data and images to the live site before review. <br>
Mitigation: Run the workflow in a scoped directory under a low-privilege account, verify the LLM and ComfyUI destinations, and inspect generated JSON before enabling automatic publishing. <br>


## Reference(s): <br>
- [Research Paper Portal on ClawHub](https://clawhub.ai/JiaxiLiao/research-paper-portal) <br>
- [OpenAlex and arXiv API guide](references/API.md) <br>
- [Configuration guide](references/CONFIG.md) <br>
- [ComfyUI Flux2 workflow guide](references/COMFYUI.md) <br>
- [OpenAlex API](https://api.openalex.org) <br>
- [arXiv API](http://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and source files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a website template, paper collection scripts, image generation workflow guidance, and scheduled publishing instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
