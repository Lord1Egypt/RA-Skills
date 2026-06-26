## Description: <br>
Analyze video content and generate a callable Skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keke-skills](https://clawhub.ai/user/keke-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to process user-provided Douyin, BiliBili, or YouTube video links, summarize the content, and generate a reusable local skill after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and processes user-provided video links through local video-processing tools and the douyin-download dependency. <br>
Mitigation: Install only when those local dependencies are trusted, and process only links intentionally supplied by the user. <br>
Risk: Generated skills persist in the OpenClaw skills directory after approval. <br>
Mitigation: Review each generated SKILL.md before approval and remove generated skills that are no longer wanted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keke-skills/video-learner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with generated SKILL.md content and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a generated SKILL.md under ~/.openclaw/workspace/skills/ after user confirmation.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
