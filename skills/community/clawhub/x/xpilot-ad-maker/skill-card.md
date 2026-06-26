## Description: <br>
Generate a 30-second cinematic ad video with consistent character, AI narration, brand overlays, and ambient music. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jytech2023](https://clawhub.ai/user/jytech2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and marketing automation users use this skill to generate short cinematic ad videos from a storyboard, brand text, and provider credentials. It is designed for customizable verticals such as medical tourism, dental tourism, cosmetic surgery, or similar service advertising workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses paid AI-provider credentials and Cloudflare R2 write access. <br>
Mitigation: Use least-privilege provider keys, a dedicated R2 bucket or prefix, and budget or quota controls before running the workflow. <br>
Risk: Prompts, narration, images, intermediate clips, and final videos leave the local machine and may become publicly reachable through the configured R2 public URL or bucket policy. <br>
Mitigation: Avoid confidential or sensitive content in prompts and generated media, and review R2 public access settings before sharing output URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jytech2023/xpilot-ad-maker) <br>
- [Publisher profile](https://clawhub.ai/user/jytech2023) <br>
- [Project homepage from skill metadata](https://github.com/dotku/x-post-scheduler/tree/main/skills/xpilot-ad-maker) <br>
- [Vidu Platform](https://platform.vidu.com) <br>
- [Example final ad output](https://pub-22e3d3e3f43e400493bbd71306cae6bb.r2.dev/demo/medical-tourism-ad/v2/medtravel-final.mp4) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files] <br>
**Output Format:** [Markdown guidance with TypeScript workflow files and shell commands; generated assets include MP4, PNG, and audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires provider API keys and Cloudflare R2 configuration; final and intermediate media are uploaded to the configured R2 bucket.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, openclaw metadata, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
