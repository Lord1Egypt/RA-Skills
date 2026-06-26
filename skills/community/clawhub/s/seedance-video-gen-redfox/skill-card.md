## Description: <br>
This skill helps agents generate MP4 videos from Chinese or English prompts using the RedFox/Seedance 2.0 video service, with controls for resolution, aspect ratio, duration, audio, watermarking, seeds, and preset avatar references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, product managers, marketers, educators, and developers can use this skill to turn text prompts into short generated videos, query generation tasks, and download completed MP4 outputs. It is suited for social media assets, product concept demos, brand visuals, creative exploration, and educational visualizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, task metadata, and referenced assets are sent to the RedFox/Seedance external service. <br>
Mitigation: Do not submit confidential, personal, or regulated material unless the service's data practices are acceptable for the use case. <br>
Risk: The skill requires an API key that could be exposed through shell history, logs, prompts, or files. <br>
Mitigation: Prefer REDFOX_API_KEY from an environment variable or secret manager, and avoid passing keys directly on the command line or storing them in plaintext. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/redfox-data/seedance-video-gen-redfox) <br>
- [RedFoxHub API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFoxHub](https://redfox.hk?source=github) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands and generated MP4 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a REDFOX_API_KEY and sends prompts, task metadata, and referenced assets to the RedFox/Seedance service.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
