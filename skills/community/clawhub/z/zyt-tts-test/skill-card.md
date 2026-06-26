## Description: <br>
Use Chanjing TTS API to convert text to speech by listing voices, creating synthesis tasks, and polling task status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuoyuting214](https://clawhub.ai/user/zuoyuting214) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn Chinese or English text into speech with Chanjing TTS, including voice selection, task creation, status polling, and retrieval of remote audio URLs and subtitle timestamps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Chanjing app_id and secret_key credentials in a local credentials file. <br>
Mitigation: Use a dedicated or revocable API key, keep the credentials file private, and use the configured private file permissions. <br>
Risk: Text submitted for synthesis is sent to Chanjing's API. <br>
Mitigation: Avoid sending sensitive text unless Chanjing's handling terms are acceptable for the user's environment. <br>
Risk: The published artifact documents helper scripts that are not present in the provided files. <br>
Mitigation: Verify available helper scripts before relying on the example commands. <br>


## Reference(s): <br>
- [Zyt TTS on ClawHub](https://clawhub.ai/zuoyuting214/zyt-tts-test) <br>
- [Chanjing Open API](https://open-api.chanjing.cc) <br>
- [Chanjing OpenAPI Login](https://www.chanjing.cc/openapi/login) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and API result values such as task IDs, remote audio URLs, and subtitles] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default behavior returns a remote audio URL and subtitles when available; local audio download is only proposed when explicitly requested.] <br>

## Skill Version(s): <br>
0.6.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
