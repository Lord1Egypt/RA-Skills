## Description: <br>
Seko Video Creation helps agents create Seko-powered video projects from text prompts, including proposal generation, asset download, proposal revision, and final video generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sekoplatform](https://clawhub.ai/user/sekoplatform) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and production teams use this skill to manage an AI video workflow from an initial idea through a Seko planning proposal and generated video. Agents can submit prompts, poll Seko task status, save JSON and Markdown project records, download image assets, modify proposals, and retrieve generated MP4 files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Seko API key and may save a .env file in the workspace. <br>
Mitigation: Use a limited or revocable SEKO_API_KEY and do not share project directories that include .env or other credential-bearing files. <br>
Risk: The skill downloads generated images and videos from URLs returned by the Seko service. <br>
Mitigation: Review downloaded media URLs and generated files before using the outputs in sensitive networks or publishing workflows. <br>
Risk: Generated proposals and videos can contain inaccurate, unwanted, or policy-sensitive creative content. <br>
Mitigation: Review proposal Markdown, generated JSON, image assets, and final MP4 files before relying on or distributing them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/sekoplatform/seko-video-creation) <br>
- [Seko API key page](https://seko.sensetime.com/explore) <br>
- [Seko creation task page](https://seko.sensetime.com/seko/creation?id=2034207127824871426) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files] <br>
**Output Format:** [Chinese-language agent guidance with Python command invocations, saved JSON task results, Markdown proposal files, downloaded images, and MP4 video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and SEKO_API_KEY; writes project files, task queues, generated media, and optional .env content inside the workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
