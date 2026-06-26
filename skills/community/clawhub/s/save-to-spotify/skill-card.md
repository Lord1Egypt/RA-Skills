## Description: <br>
Create polished audio content and save it to Spotify with TTS narration, rich playback timelines, cover images, and show or episode management support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spotify](https://clawhub.ai/user/spotify) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn authorized source material or local audio into Spotify-hosted episodes. It guides agents through interviewing the user, scripting, generating or assembling audio, creating cover artwork, writing HTML descriptions, building timeline companions, and saving the result with the Spotify CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Spotify OAuth credentials and can use those credentials for account-backed Spotify operations. <br>
Mitigation: Authenticate deliberately, avoid printing or storing tokens in shared logs, and revoke or refresh credentials if exposure is suspected. <br>
Risk: The workflow can upload or delete Spotify show and episode data. <br>
Mitigation: Confirm the destination show and any destructive operation before running Spotify CLI commands; review JSON output before follow-up actions. <br>
Risk: The recommended one-line installer executes a remote shell script. <br>
Mitigation: Prefer manually downloaded, version-pinned releases and review release artifacts or checksums before installation. <br>
Risk: Cloud TTS or image providers may receive scripts, source material, or generated episode assets. <br>
Mitigation: Use local or offline providers for confidential material and avoid sending sensitive content to external generation services. <br>
Risk: Generated audio and descriptions can misrepresent source material or rights if sourcing is weak. <br>
Mitigation: Use only authorized source material, preserve source links, avoid fabricated URLs, and review the script and description before upload. <br>


## Reference(s): <br>
- [Save To Spotify on ClawHub](https://clawhub.ai/spotify/save-to-spotify) <br>
- [Spotify publisher profile](https://clawhub.ai/user/spotify) <br>
- [CLI usage](references/cli-usage.md) <br>
- [Spotify Web API](references/spotify-api.md) <br>
- [Audio providers and assembly](references/audio-providers.md) <br>
- [Cover image](references/cover-image.md) <br>
- [Timeline format](references/timeline.md) <br>
- [Episode description format](references/episode-description.md) <br>
- [Content quality guidelines](references/content-quality.md) <br>
- [Spotify Developer LLM entrypoint](https://developer.spotify.com/llms.txt) <br>
- [Spotify Web API OpenAPI schema](https://developer.spotify.com/reference/web-api/open-api-schema.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON examples, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in generated audio files, cover images, timeline.json, HTML descriptions, and Spotify show or episode updates when the agent executes the workflow.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
