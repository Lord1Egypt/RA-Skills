## Description: <br>
Use Chanjing video synthesis APIs to create digital human videos from text or audio, with optional background upload, task polling, and explicit download when the user asks to save the result locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuoyuting214](https://clawhub.ai/user/zuoyuting214) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create Chanjing digital human videos from text or local audio, choose public or custom digital figures, upload optional media, poll generation status, and save the result only when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses local Chanjing API credentials and may cache access tokens. <br>
Mitigation: Use a dedicated or revocable Chanjing API key when possible and protect the credentials file. <br>
Risk: The skill uploads user-selected audio or background media to Chanjing for video generation. <br>
Mitigation: Upload only media that the user explicitly intends to process and avoid sensitive files unless the target service is approved for that data. <br>
Risk: Some documented helper commands may not be present in the artifact files. <br>
Mitigation: Confirm available scripts and inspect any added helper scripts before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zuoyuting214/zyt-video-compose) <br>
- [Chanjing Open API](https://open-api.chanjing.cc) <br>
- [Reference](reference.md) <br>
- [Examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Chanjing figure IDs, file IDs, video task IDs, video URLs, and local output paths when download is explicitly requested.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
