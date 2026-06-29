## Description: <br>
Use when a user wants to connect to or use Wubble's official remote MCP server for music, speech, voice, dubbing, and sound-effect workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wubbletech](https://clawhub.ai/user/wubbletech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect agents to Wubble's remote MCP audio service, configure the official endpoint or registry name, complete OAuth in the MCP client, and distinguish read-only actions from media-generation actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The remote MCP service can create media or consume Wubble requests or credits. <br>
Mitigation: Confirm the user's intent and requested output before generation, upload, remix, dubbing, speech, or other spendful actions. <br>
Risk: OAuth tokens, API keys, signed media URLs, private media, prompts, lyrics, transcripts, or voice data may be sensitive. <br>
Mitigation: Use client-provided OAuth when available, avoid asking for secrets, and do not log, store, or reveal sensitive media or credential data unless explicitly approved by the user. <br>
Risk: Generated or downloaded media may have usage, ownership, commercial-use, or licensing restrictions under Wubble's terms. <br>
Mitigation: Review Wubble's Terms of Use and Subscriber License before relying on generated or downloaded media commercially, and direct legal questions to those documents rather than improvising legal advice. <br>


## Reference(s): <br>
- [Wubble remote MCP endpoint](https://mcp.wubble.ai/mcp) <br>
- [Wubble public health endpoint](https://mcp.wubble.ai/health) <br>
- [Wubble Terms of Use](https://wubble.ai/docs/legal/terms) <br>
- [Wubble Subscriber License](https://wubble.ai/docs/legal/license) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with inline text and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes official MCP connection details, OAuth handling guidance, safe-use checks, and legal-reference pointers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
