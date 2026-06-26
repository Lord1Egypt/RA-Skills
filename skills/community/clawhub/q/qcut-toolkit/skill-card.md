## Description: <br>
QCut Toolkit routes agents across project organization, FFmpeg media processing, AI content generation and analysis, QCut editor control, video prompt writing, MCP preview testing, and PR comment workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donghaozhang](https://clawhub.ai/user/donghaozhang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and media creators use this skill to choose and run QCut workflows for organizing projects, transforming media, generating or analyzing AI media, preparing subtitles, and controlling editor-related tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media and audio may be uploaded to public or third-party services. <br>
Mitigation: Use only non-confidential inputs unless the upload path is replaced with approved private storage and reviewed service providers. <br>
Risk: API keys and credentials are required for several media and AI workflows. <br>
Mitigation: Store keys in approved credential stores, avoid printing or committing secrets, and rotate exposed credentials. <br>
Risk: Persistent skill or rule-file updates could change future agent behavior. <br>
Mitigation: Review proposed changes to CLAUDE.md and skill rule files before accepting them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/donghaozhang/qcut-toolkit) <br>
- [QCut Toolkit skill definition](artifact/SKILL.md) <br>
- [AI Content Pipeline reference](artifact/ai-content-pipeline/REFERENCE.md) <br>
- [AI Content Pipeline examples](artifact/ai-content-pipeline/EXAMPLES.md) <br>
- [FFmpeg command reference](artifact/ffmpeg-skill/REFERENCE.md) <br>
- [FFmpeg concepts](artifact/ffmpeg-skill/CONCEPTS.md) <br>
- [MCP preview testing guide](artifact/qcut-mcp-preview-test/SKILL.md) <br>
- [Video cut talk-edit workflow](artifact/videocut/talk-edit/SKILL.md) <br>
- [Video subtitle workflow](artifact/videocut/subtitles/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local media files, subtitles, review artifacts, or editor project changes when the user approves the workflow commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
