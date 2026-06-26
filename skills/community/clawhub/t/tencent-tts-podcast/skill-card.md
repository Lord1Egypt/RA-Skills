## Description: <br>
Convert text to podcast audio using Tencent Cloud TTS, with short-text and long-text processing, automatic chunking, parallel generation, and support for 26 Chinese voices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[isLinXu](https://clawhub.ai/user/isLinXu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert supplied text into WAV podcast-style speech through Tencent Cloud TTS, including longer scripts that need chunking and retry handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text is processed by Tencent Cloud TTS, so confidential content may leave the local environment. <br>
Mitigation: Only process confidential text when Tencent Cloud handling is acceptable for the use case. <br>
Risk: Optional Tencent COS upload may expose generated audio because the code attempts a public-read ACL. <br>
Mitigation: Leave COS upload disabled unless cloud storage and sharing are intentional, and review bucket permissions before use. <br>
Risk: The skill installs Python dependencies and uses cloud credentials. <br>
Mitigation: Install in an isolated Python environment, review or pin dependencies, and use least-privilege Tencent credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/isLinXu/tencent-tts-podcast) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Configuration, Audio files, API calls] <br>
**Output Format:** [JSON status object plus generated WAV audio file path or URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud credentials; optional COS upload can return a cloud URL instead of a local file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
