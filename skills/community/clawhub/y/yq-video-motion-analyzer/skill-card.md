## Description: <br>
Yq Video Motion Analyzer helps an agent extract key frames from sports teaching videos, analyze motion posture, and generate stick-figure diagrams with improvement feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, coaches, athletes, and instructional video reviewers use this skill to break down sports teaching videos into key frames, posture analysis, strengths, issues, and targeted improvement guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided videos and extracted frames may contain sensitive visual content and may be processed by the host's configured video or image understanding tools. <br>
Mitigation: Use only videos the user is authorized to analyze, and review the host environment's video and image tool data-handling settings before processing sensitive material. <br>
Risk: Frame extraction writes local image files that can persist after the analysis is complete. <br>
Mitigation: Choose the output directory deliberately, restrict access to generated frame and diagram folders, and delete generated images when they are no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JSON-style analysis summaries, shell commands, extracted frame images, and generated PNG diagrams] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates JPEG frames under output/frames and PNG stick-figure diagrams under output/stickman.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, _meta.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
