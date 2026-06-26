## Description: <br>
Seedream 图片生成 - 火山引擎方舟大模型服务平台图片生成 API。支持文生图、图生图、多图融合、组图生成等多种模式。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xhuang68](https://clawhub.ai/user/xhuang68) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to call Volcengine Ark Seedream image generation for text-to-image, image-to-image, multi-image fusion, sequential image generation, and web-search-assisted generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts, image URLs, and referenced images are sent to Volcengine Ark/Seedream for processing. <br>
Mitigation: Use the skill only when that external processing is acceptable, and avoid regulated data, private internal URLs, confidential images, and secrets in prompts or image inputs. <br>
Risk: Passing ARK_API_KEY on the command line can expose the credential through shell history or process listings. <br>
Mitigation: Prefer setting ARK_API_KEY in the environment instead of passing the API key as a command-line argument. <br>


## Reference(s): <br>
- [Volcengine Seedream image generation documentation](https://www.volcengine.com/docs/82379/1541523) <br>
- [ClawHub release page](https://clawhub.ai/xhuang68/seedream-image-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash code blocks and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and ARK_API_KEY; generated images are saved to the requested output directory, defaulting to ~/Downloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
