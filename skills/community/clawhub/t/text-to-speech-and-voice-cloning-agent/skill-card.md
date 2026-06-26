## Description: <br>
Turn your AI assistant into a TTS and voice cloning powerhouse using the Verbatik API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[verbatik](https://clawhub.ai/user/verbatik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to generate speech, clone voices from permitted audio, manage cloned voices, browse available Verbatik voices, and check prepaid account balance through the Verbatik API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent sensitive voice-cloning and cloned-voice deletion authority without built-in consent or confirmation safeguards. <br>
Mitigation: Require explicit confirmation before cloning a voice, storing or sharing generated audio, deleting a cloned voice, or spending prepaid balance; only clone voices when documented speaker permission exists. <br>
Risk: The Verbatik API key can authorize paid operations against a prepaid balance. <br>
Mitigation: Keep VERBATIK_API_KEY scoped and protected, estimate cost before large batches, and check balance before bulk operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/verbatik/text-to-speech-and-voice-cloning-agent) <br>
- [Verbatik API](https://api.verbatik.com) <br>
- [Verbatik MCP Endpoint](https://api.verbatik.com/api/mcp/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API calls, Text] <br>
**Output Format:** [Markdown instructions with HTTP request examples and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VERBATIK_API_KEY; generated audio may be returned as binary audio or stored audio URLs depending on API request headers.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
