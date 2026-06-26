## Description: <br>
Voicenotes Official lets OpenClaw search Voicenotes notes semantically, retrieve transcripts, filter notes by tags or date range, and create text notes through the Voicenotes API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gthu-vn](https://clawhub.ai/user/gthu-vn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users with a Voicenotes account use this skill to search their notes, retrieve full transcripts when needed, filter recordings by tags or date range, and create text notes from natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Voicenotes API key that can access notes and transcripts in the user's account. <br>
Mitigation: Use a revocable or dedicated API key when available, avoid storing secrets in notes, and revoke the key if access is no longer needed. <br>
Risk: Broad transcript retrieval or note creation can expose or modify personal account content. <br>
Mitigation: Ask the agent to confirm before broad transcript retrieval or note creation. <br>
Risk: Unsanitized user input in shell commands can alter API requests. <br>
Mitigation: URL-encode search queries, validate recording IDs against the documented alphanumeric pattern, and JSON-encode request bodies. <br>


## Reference(s): <br>
- [Voicenotes](https://voicenotes.com) <br>
- [Voicenotes OpenClaw integration setup](https://voicenotes.com/app?open-claw=true#settings) <br>
- [ClawHub skill page](https://clawhub.ai/gthu-vn/voicenotes-official) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/gthu-vn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands, JSON examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses VOICENOTES_API_KEY and curl to call Voicenotes API endpoints.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
