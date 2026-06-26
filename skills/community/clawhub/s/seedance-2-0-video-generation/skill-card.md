## Description: <br>
Generates AI videos with ByteDance Seedance 2.0 from text or images, including long videos by sequencing shorter segments and reusing each segment's final frame for continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liusaikang](https://clawhub.ai/user/liusaikang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and creative operators use this skill to create Seedance 2.0 video-generation tasks, monitor completion, download outputs, and build longer videos from sequential segments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and image inputs are sent to Volcengine/ByteDance services. <br>
Mitigation: Use only prompts and images that are approved for external processing, and prefer a scoped Ark API key where possible. <br>
Risk: Downloaded outputs may be written to user-selected paths. <br>
Mitigation: Choose a non-sensitive output directory and review generated files before sharing or reusing them. <br>
Risk: The reviewed artifact includes an automatic file-opening step on macOS that can invoke the shell with a user-controlled download path. <br>
Mitigation: Avoid unusual download paths on macOS until the automatic open behavior is removed or replaced with a non-shell implementation. <br>
Risk: Antivirus confirmation was pending in the security evidence. <br>
Mitigation: Review and scan the skill before installation or deployment. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/liusaikang/seedance-2-0-video-generation) <br>
- [Volcengine Ark API endpoint](https://ark.cn-beijing.volces.com/api/v3) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python CLI and curl command examples; generated artifacts may include MP4 video files, PNG last-frame images, and sequence_manifest.json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ARK_API_KEY for Volcengine Ark API access and supports asynchronous task polling, downloads, and serialized long-video generation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
