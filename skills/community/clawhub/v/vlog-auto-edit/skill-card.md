## Description: <br>
Guides an agent through a travel-vlog editing workflow that analyzes raw footage, plans a narrative edit, previews the result, and renders a finished video with ffmpeg and Python tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[znyupup](https://clawhub.ai/user/znyupup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and agent users use this skill to turn a folder of travel or daily-life video clips into a structured vlog. The workflow helps the agent inspect footage, transcribe speech, request visual descriptions, draft an edit plan, generate review dashboards, and produce a final video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected video frames may be sent to the user's chosen vision API. <br>
Mitigation: Use a limited API key, review the provider's retention policy, and avoid sensitive footage unless sharing it is approved. <br>
Risk: The workflow reads footage folders and generates local transcripts, thumbnails, dashboards, and rendered videos. <br>
Mitigation: Run it only on footage the user intends to process and review generated dashboards and plans before final rendering or sharing. <br>
Risk: The skill may install media packages and execute ffmpeg or Python commands. <br>
Mitigation: Review commands and dependency changes before execution, especially in shared or production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/znyupup/vlog-auto-edit) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/znyupup) <br>
- [Author link from ClawHub metadata](https://github.com/znyupup) <br>
- [Skill workflow](artifact/SKILL.md) <br>
- [Project README](artifact/README.md) <br>
- [Edit plan prompt template](artifact/templates/edit_plan_prompt.md) <br>
- [Vision API provider referenced by documentation](https://open.bigmodel.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, HTML, video files] <br>
**Output Format:** [Markdown guidance with bash and Python snippets, JSON edit plans, generated HTML previews, and rendered video artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local footage and local generated assets; selected frames may be sent to a user-selected vision API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
