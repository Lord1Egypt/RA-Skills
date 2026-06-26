## Description: <br>
Generate and build Pulse Apps using the Vibe Dev Flow API. Use this skill when the user wants to create, update, or generate code for Pulse Editor applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shellishack](https://clawhub.ai/user/Shellishack) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI coding agents use this skill to create, update, build, and publish Pulse Editor applications through the Pulse Editor Vibe Dev Flow API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to the Pulse Editor cloud API. <br>
Mitigation: Avoid including secrets, regulated data, or other sensitive information in prompts. <br>
Risk: The skill can publish or update live Pulse Editor apps. <br>
Mitigation: Explicitly confirm requests that update an existing app or publish a live app before calling the API. <br>
Risk: The API requires a Pulse Editor API key. <br>
Mitigation: Provide the API key through an environment variable or credential manager and do not hardcode it in prompts, scripts, or generated files. <br>


## Reference(s): <br>
- [Pulse Editor skill page](https://clawhub.ai/Shellishack/pulse-editor) <br>
- [Pulse Editor documentation](https://docs.pulse-editor.com/) <br>
- [Pulse Editor API reference](https://docs.pulse-editor.com/api-reference) <br>
- [Get Pulse Editor API key](https://docs.pulse-editor.com/api-reference/get-pulse-editor-api-key) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads, shell commands, and Python or JavaScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SSE streaming and can return final artifact details such as published app link, source archive link, app ID, and version.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
