## Description: <br>
Generate standalone speech audio from text with HeyGen's Starfish TTS model, including voice selection, speed control, language and locale options, and SSML support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelwang11394](https://clawhub.ai/user/michaelwang11394) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to list HeyGen Starfish-compatible voices and convert text or SSML into speech audio for voiceovers, narration, podcasts, captions, or timed media workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided text to HeyGen's external text-to-speech API. <br>
Mitigation: Avoid converting sensitive text unless HeyGen's data handling is acceptable for the intended use case. <br>
Risk: The skill requires a HeyGen API key for voice listing and speech generation. <br>
Mitigation: Use an appropriately scoped API key and store it in the HEYGEN_API_KEY environment variable rather than embedding it in prompts or code. <br>
Risk: Broad HeyGen tool access could expose more functionality than needed for text-to-speech workflows. <br>
Mitigation: Where the agent environment supports narrower permissions, limit access to the HeyGen voice-listing and text-to-speech tools. <br>


## Reference(s): <br>
- [ClawHub listing: Text to Speech](https://clawhub.ai/michaelwang11394/text-to-speech-heygen) <br>
- [Publisher profile: michaelwang11394](https://clawhub.ai/user/michaelwang11394) <br>
- [HeyGen voice listing endpoint](https://api.heygen.com/v3/voices?engine=starfish) <br>
- [HeyGen text-to-speech endpoint](https://api.heygen.com/v3/voices/speech) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with curl, TypeScript, and Python examples; HeyGen API responses return JSON containing audio URLs and timing metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HEYGEN_API_KEY and produces or retrieves speech audio through HeyGen's external API.] <br>

## Skill Version(s): <br>
2.23.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
