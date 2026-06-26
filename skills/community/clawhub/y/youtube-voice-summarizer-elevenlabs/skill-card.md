## Description: <br>
Transform YouTube videos into podcast-style voice summaries using ElevenLabs TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Franciscoandsam](https://clawhub.ai/user/Franciscoandsam) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use this skill to turn YouTube links into concise text summaries or podcast-style audio summaries with configurable length and voice options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The backend requires API keys for ElevenLabs, Supadata, and OpenRouter. <br>
Mitigation: Store keys outside prompts and skill text, restrict access to the backend environment, and rotate keys if they are exposed. <br>
Risk: Summarization and text-to-speech rely on third-party services that may process submitted YouTube content. <br>
Mitigation: Avoid private, sensitive, or regulated content unless the operator has reviewed and accepted the relevant service terms and data handling. <br>
Risk: External backend dependencies and npm packages can change independently of this skill release. <br>
Mitigation: Review the backend repository and lock or scan dependencies before deployment. <br>
Risk: Usage of third-party transcript, model, and voice services can incur variable costs. <br>
Mitigation: Set spending limits or quotas where supported and monitor usage for unexpected volume. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Franciscoandsam/youtube-voice-summarizer-elevenlabs) <br>
- [Publisher profile](https://clawhub.ai/user/Franciscoandsam) <br>
- [ElevenLabs](https://elevenlabs.io) <br>
- [Supadata](https://supadata.ai) <br>
- [OpenRouter](https://openrouter.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Audio URL] <br>
**Output Format:** [Markdown responses with curl examples, JSON API results, text summaries, key points, and MP3 audio URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a deployed backend service and API keys for ElevenLabs, Supadata, and OpenRouter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
