## Description: <br>
Captures user facts, preferences, and procedural corrections into local .reflexio/ memory so an OpenClaw agent can learn across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yyiilluu](https://clawhub.ai/user/yyiilluu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Reflexio to preserve durable preferences, facts, and corrected workflows across OpenClaw sessions. It writes and retrieves local profile and playbook memories so future agent runs can adapt to the user's established context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically processes transcripts and can rewrite or delete long-term memory. <br>
Mitigation: Review what may be stored in .reflexio/, back up existing .reflexio data before enabling, and inspect memory changes after consolidation. <br>
Risk: Transcript or memory content may be sent to the configured model provider during extraction, deduplication, or consolidation. <br>
Mitigation: Confirm the model provider data-handling policy before use and avoid storing secrets, tokens, private keys, environment variables, or unnecessary sensitive personal data. <br>
Risk: The plugin may add a heartbeat task to the workspace and periodically consolidate memory. <br>
Mitigation: Enable it only when automatic long-term memory is intended, and review the workspace task and consolidation settings during setup. <br>


## Reference(s): <br>
- [ClawHub Reflexio listing](https://clawhub.ai/yyiilluu/reflexio) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [Reflexio OpenClaw embedded source reference](https://github.com/ReflexioAI/reflexio/tree/main/reflexio/integrations/openclaw-embedded) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown memory entries, concise agent guidance, and optional shell commands or configuration changes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local .reflexio/ profile and playbook files; profile entries may include TTL metadata.] <br>

## Skill Version(s): <br>
1.0.10 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
