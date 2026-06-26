## Description: <br>
Use this skill to generate high-quality AI videos using the SeaArt platform (seaart.ai), including Text-to-Video and Image-to-Video generation with multiple models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foxwzh](https://clawhub.ai/user/foxwzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to submit text-to-video or image-to-video jobs to SeaArt, choose supported video models and aspect ratios, and receive the generated video URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The SeaArt session token represents account access and is sent as a cookie to SeaArt API endpoints. <br>
Mitigation: Store SEAART_TOKEN only in the local agent configuration, avoid printing it in logs or chat, and rotate or revoke the SeaArt session if it is exposed. <br>
Risk: Prompts and image URLs provided for generation are sent to SeaArt. <br>
Mitigation: Use the skill only when the user trusts SeaArt with the prompt, image URLs, and generated content workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/foxwzh/seaart-video) <br>
- [SeaArt platform](https://www.seaart.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and a final generated video URL as text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SEAART_TOKEN and a SeaArt account; the Python helper polls SeaArt until completion or timeout.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
