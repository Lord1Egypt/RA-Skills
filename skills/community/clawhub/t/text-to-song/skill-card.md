## Description: <br>
AI music generation assistant powered by MakebestMusic for creating AI-generated music, songs, and audio tracks from text prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sthk-mbm](https://clawhub.ai/user/sthk-mbm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content creators, musicians, and developers use this skill to generate custom songs or instrumental audio tracks from text prompts and check generation status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Song descriptions and generation identifiers are sent to MakebestMusic using the configured API key. <br>
Mitigation: Avoid sensitive personal or proprietary information in prompts and use a dedicated, revocable API key where possible. <br>
Risk: The skill can use an alternate API endpoint when MBM_API_BASE is set. <br>
Mitigation: Set MBM_API_BASE only when you intentionally trust the alternate endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sthk-mbm/text-to-song) <br>
- [MakeBestMusic website](https://makebestmusic.com/?pid=PIDcLjhgCXUQ) <br>
- [MakeBestMusic API endpoint](https://api.makebestmusic.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON script responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured MakeBestMusic API key and may return generation IDs, status values, and hosted music links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and changelog mention 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
