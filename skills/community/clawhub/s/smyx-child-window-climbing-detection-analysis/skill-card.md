## Description: <br>
This skill analyzes fixed-camera images or videos of windows and balconies to detect child climbing, leaning, railing-crossing, gripping, and other high-fall-risk behaviors, then returns structured alerts and report links when available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and caretaking teams use this skill to analyze fixed-camera images or videos of window and balcony areas for child climbing, leaning, railing-crossing, and other high-fall-risk behaviors. It returns structured detection results, alert levels, report links when available, and cloud history lookup output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud processing of child-monitoring images or videos may expose sensitive minor-related media outside the local workspace. <br>
Mitigation: Use only media for which guardians have consented, prefer a dedicated workspace/account, and avoid private household camera feeds unless cloud processing is acceptable. <br>
Risk: The skill silently associates requests with an account identity and stores authentication material locally for reuse. <br>
Mitigation: Run it in a dedicated workspace, limit workspace access, and remove local data/token files when you stop using the skill. <br>
Risk: History lookup returns cloud report history linked to the resolved identity. <br>
Mitigation: Treat report links, snapshots, and exported reports as sensitive child-safety records and share them only with authorized guardians or operators. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-child-window-climbing-detection-analysis) <br>
- [API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown and JSON text with optional report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs analysis results, alert status, history listings, and optional local result files when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
