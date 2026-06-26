## Description: <br>
This official skill from the Voicenotes team gives OpenClaw access to Voicenotes APIs for semantic search, transcript retrieval, tag or date filtering, and text-note creation through natural conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kscoggins](https://clawhub.ai/user/kscoggins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to search, retrieve, filter, and create notes in their own Voicenotes account through authenticated API requests. It supports semantic search, transcript lookup, tag and date filtering, and text-note creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses VOICENOTES_API_KEY to search, read, and create notes in a user's Voicenotes account, so exposure of the key can expose private notes or allow note creation. <br>
Mitigation: Treat the API key like a password, provide it only through the configured skill environment, and revoke or rotate it when no longer needed. <br>
Risk: Write actions can create new notes in the user's account. <br>
Mitigation: Ask the agent to confirm before creating a note and review note content before sending the request. <br>
Risk: User-provided search text, recording IDs, tags, dates, or note content are placed into API requests. <br>
Mitigation: URL-encode search parameters, validate recording IDs, and JSON-encode body fields rather than interpolating raw input into shell commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kscoggins/voicenotes-official-1-0-3) <br>
- [Voicenotes homepage](https://voicenotes.com) <br>
- [Voicenotes OpenClaw integration setup](https://voicenotes.com/app?open-claw=true#settings) <br>
- [Voicenotes OpenClaw semantic search endpoint](https://api.voicenotes.com/api/integrations/open-claw/search/semantic) <br>
- [Voicenotes OpenClaw recordings endpoint](https://api.voicenotes.com/api/integrations/open-claw/recordings) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl commands, YAML configuration snippets, JSON request bodies, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and VOICENOTES_API_KEY; authenticated API responses may include private note content.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
