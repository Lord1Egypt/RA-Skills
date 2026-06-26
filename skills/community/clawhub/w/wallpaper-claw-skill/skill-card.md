## Description: <br>
Generate AI wallpaper images from a text prompt via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[barbaraledbettergq](https://clawhub.ai/user/barbaraledbettergq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate wallpaper image URLs from text prompts through the Neta/TalesOfAI image service, with optional size and reference-image controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallpaper prompts, optional reference IDs, and the Neta/TalesOfAI API token are sent to api.talesofai.com. <br>
Mitigation: Use a revocable service-specific token and only submit prompts and reference IDs that are appropriate to share with the third-party image service. <br>
Risk: Passing tokens on the command line can expose them through shell history, logs, or shared terminal environments. <br>
Mitigation: Avoid shared machines and logged terminals or CI for token use; rotate the token if it may have been recorded. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/barbaraledbettergq/wallpaper-claw-skill) <br>
- [Neta AI access page](https://www.neta.art/open/) <br>
- [TalesOfAI API host](https://api.talesofai.com) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls] <br>
**Output Format:** [Plain text URL or JSON status object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs to stdout after polling the image-generation task; results may include a generated image URL, task UUID, dimensions, and status depending on the script used.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
