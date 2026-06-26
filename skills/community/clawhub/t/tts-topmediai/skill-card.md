## Description: <br>
TopMediai text-to-speech skill that supports API key entitlement checks, official and cloned voice listing, and text-to-speech generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Topmediai](https://clawhub.ai/user/Topmediai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to check TopMediai API key entitlement, inspect available official and cloned voices, and request text-to-speech synthesis with a selected speaker and optional emotion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Synthesis text, selected voice data, and the TopMediai API key are sent to the configured TopMediai endpoint. <br>
Mitigation: Use a dedicated API key where possible, keep the .env file private, avoid sensitive text, and leave TOPMEDIAI_BASE_URL set to the official service unless another endpoint is trusted. <br>
Risk: Debug output can expose private request content when TOPMEDIAI_DEBUG is enabled. <br>
Mitigation: Keep TOPMEDIAI_DEBUG disabled when processing private or sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/Topmediai/tts-topmediai) <br>
- [Topmediai publisher profile](https://clawhub.ai/user/Topmediai) <br>
- [TopMediai API endpoint](https://api.topmediai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Text command responses containing JSON from TopMediai API operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-to-speech requests require configured TopMediai API credentials and send synthesis text, speaker, and optional emotion to the configured endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
