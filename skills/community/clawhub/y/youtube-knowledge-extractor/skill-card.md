## Description: <br>
Multimodal YouTube video analysis through transcript extraction, frame extraction, and synchronized audio-visual analysis for summaries, tutorials, demos, and step-by-step guides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdrabent](https://clawhub.ai/user/sdrabent) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and knowledge workers use this skill to analyze YouTube videos, extract transcripts and frames, and produce summaries, technical analyses, or step-by-step guides that combine what is said with what is shown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may download YouTube transcripts, video data, and frame images to the local machine. <br>
Mitigation: Use the skill only for videos the user is authorized to analyze, keep work in temporary directories, and remove temporary files after the analysis. <br>
Risk: Browser-cookie access can expose an authenticated YouTube session to the agent workflow. <br>
Mitigation: Use browser cookies only when explicitly needed for a video the user is authorized to view, and avoid cookie access for public videos. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdrabent/youtube-knowledge-extractor) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with timestamped sections, visual anchors, and inline shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transcript-derived summaries, frame observations, synchronized audio-visual notes, and visual-only findings.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
