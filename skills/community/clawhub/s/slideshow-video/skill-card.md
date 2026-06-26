## Description: <br>
Generate TikTok-style slideshow assets and MP4 exports from local images, GPT Image 2 visuals, remote image URLs, or lightweight image queries plus structured copy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and content teams use this skill to turn structured project JSON, source images, generated visuals, and narration assets into platform-ready slideshow PNGs, short vertical MP4 exports, and handoff metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release asks users to run external setup that may involve API keys. <br>
Mitigation: Review the external repository and environment setup before use, protect API keys from commits and logs, and avoid installing or running unreviewed dependencies in trusted environments. <br>
Risk: Project files can reference local files, remote media URLs, and generated caches. <br>
Mitigation: Use only trusted project JSON files, avoid private or internal media URLs, and inspect generated caches and outputs before publishing or sharing. <br>
Risk: The security verdict is suspicious due to under-scoped file and network behavior. <br>
Mitigation: Run the skill in a restricted workspace, review planned file and network access before execution, and scan generated artifacts before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/x-rayluan/slideshow-video) <br>
- [Pipeline example](references/pipeline.example.json) <br>
- [Slides config example](references/slides-config.example.json) <br>
- [Workflow guide](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents toward generated slide PNGs, MP4 files, resolved project JSON, summary metadata, and cached remote media.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
