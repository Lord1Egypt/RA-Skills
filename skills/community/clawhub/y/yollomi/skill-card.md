## Description: <br>
Generates images and videos through the Yollomi API using a unified endpoint across multiple image and video models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AniChikage](https://clawhub.ai/user/AniChikage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to generate or transform images and create videos through Yollomi models from prompts, image URLs, and model-specific parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generation prompts, image URLs, and image or video inputs are sent to Yollomi or the configured YOLLOMI_BASE_URL. <br>
Mitigation: Use the skill only with prompts and media that are appropriate to send to that service, and avoid untrusted base URL overrides. <br>
Risk: Video and multi-output generation requests can consume substantial credits. <br>
Mitigation: Confirm the selected model, generation type, and output count before running requests. <br>
Risk: The skill requires a YOLLOMI_API_KEY for generation requests. <br>
Mitigation: Keep the API key private and provide it through the environment rather than embedding it in prompts or files. <br>


## Reference(s): <br>
- [Yollomi skill page](https://clawhub.ai/AniChikage/yollomi) <br>
- [AniChikage publisher profile](https://clawhub.ai/user/AniChikage) <br>
- [Models reference](models-reference.md) <br>
- [Skill instructions](SKILL.md) <br>
- [Yollomi service endpoint](https://yollomi.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Generated images, Generated videos, JSON] <br>
**Output Format:** [JSON responses containing image URL arrays, video URL strings, model lists, and remaining credit counts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YOLLOMI_API_KEY. YOLLOMI_BASE_URL may override the default Yollomi host.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
