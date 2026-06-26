## Description: <br>
Translates subtitles in an existing public HTTPS video through WeryAI using the video-subtitle-translate workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill when a user needs subtitles in an existing public HTTPS video translated to a target language with WeryAI. It is scoped to subtitle translation and not subtitle removal, local file upload, or new video generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a public video URL to WeryAI for paid external processing. <br>
Mitigation: Use dry-run first when practical and confirm the exact video URL and target language before submit or wait commands. <br>
Risk: The WERYAI_API_KEY credential is required for real API calls. <br>
Mitigation: Keep WERYAI_API_KEY only in the runtime environment and do not write it into files or prompts. <br>


## Reference(s): <br>
- [WeryAI llms.txt](https://docs.weryai.com/llms.txt) <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/video-tool-subtitle-translate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include WeryAI task IDs, status, error details, and final video URLs; dry-run mode previews the API request without submitting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
