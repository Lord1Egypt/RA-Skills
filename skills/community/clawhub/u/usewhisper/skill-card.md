## Description: <br>
Official Whisper Context skill for OpenClaw. Cuts context tokens via delta compression + caching, and adds long-term memory across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Alinxus](https://clawhub.ai/user/Alinxus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to retrieve compressed context, persist selected conversation turns as memory, search memories, run Oracle search, and inspect cost or cache information through a Node-based helper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected conversation content and memories are sent to the hosted Whisper Context API as the skill's core function. <br>
Mitigation: Install only if the service is trusted with the conversations and memories sent to it, and avoid sending secrets or arbitrary local files through stdin or @path inputs. <br>
Risk: The helper authenticates with a user-provided API key and can target a configurable API URL. <br>
Mitigation: Use a least-privilege API key, keep it out of source control, and keep WHISPER_CONTEXT_API_URL pointed at a trusted endpoint. <br>
Risk: The helper can auto-create a project when the configured project is not found. <br>
Mitigation: Confirm automatic project creation is acceptable for the organization before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Alinxus/usewhisper) <br>
- [Publisher profile](https://clawhub.ai/user/Alinxus) <br>
- [Whisper Context API endpoint](https://context.usewhisper.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require Node, WHISPER_CONTEXT_API_KEY, and WHISPER_CONTEXT_PROJECT; WHISPER_CONTEXT_API_URL is optional.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
