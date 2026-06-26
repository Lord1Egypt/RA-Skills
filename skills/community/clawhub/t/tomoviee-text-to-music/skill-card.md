## Description: <br>
Generate background music from text prompts using Tomoviee Text-to-Music API (`tm_text2music`) through Wondershare OpenAPI gateway (`https://openapi.wondershare.cc`). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create Tomoviee text-to-music tasks, poll asynchronous task status, and retrieve generated audio URLs for user-supplied music prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API credentials can be exposed through shell history, shared logs, committed files, or copied prompts. <br>
Mitigation: Use dedicated Tomoviee/Wondershare API credentials, prefer environment variables or secret stores, and avoid passing real secrets directly in shared shell commands or logs. <br>
Risk: Callback URLs and callback parameters can disclose task data or route notifications to unintended systems. <br>
Mitigation: Provide only callback URLs you control and avoid placing sensitive information in prompts or callback parameters. <br>


## Reference(s): <br>
- [Tomoviee Text-to-Music API Reference](references/audio_apis.md) <br>
- [Tomoviee Prompt Engineering Guide](references/prompt_guide.md) <br>
- [Tomoviee Developer Portal](https://www.tomoviee.ai/developers.html) <br>
- [Tomoviee API Documentation](https://www.tomoviee.ai/doc/) <br>
- [Tomoviee Mainland Developer Portal](https://www.tomoviee.cn/developers.html) <br>
- [Tomoviee Mainland API Documentation](https://www.tomoviee.cn/doc/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python and bash examples; API responses are JSON-like task data and generated audio URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tomoviee/Wondershare API credentials; prompts support up to 77 tokens, duration is 0-95 seconds, and quantity is 1-4 tracks.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
