## Description: <br>
AI music generation assistant powered by MakebestMusic for creating AI-generated songs and audio tracks from text prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sthk-mbm](https://clawhub.ai/user/sthk-mbm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content creators, and musicians use this skill to generate vocal or instrumental music from text prompts and check task status until shared music links are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Song prompts, lyrics, personal data, proprietary creative material, and the MakeBestMusic API key may be sent to a third-party service. <br>
Mitigation: Install only if the publisher is trusted, avoid confidential or proprietary prompt content, and protect the user-provided apiKey. <br>
Risk: The MBM_API_BASE environment variable can redirect requests to a custom endpoint. <br>
Mitigation: Set MBM_API_BASE only to endpoints the user controls or trusts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sthk-mbm/texttomusic) <br>
- [MakeBestMusic](https://makebestmusic.com/?pid=PIDcLjhgCXUQ) <br>
- [MakeBestMusic API endpoint](https://api.makebestmusic.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided apiKey and returns task identifiers, status values, and shared music URLs when generation completes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
