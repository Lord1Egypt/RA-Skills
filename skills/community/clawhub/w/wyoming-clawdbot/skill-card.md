## Description: <br>
Wyoming Protocol bridge for Home Assistant voice assistant integration with Clawdbot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vglafirov](https://clawhub.ai/user/vglafirov) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Home Assistant users use this skill to run a Wyoming Protocol bridge that sends Home Assistant Assist transcripts to Clawdbot and returns responses for text-to-speech. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Network-received voice prompts can expose a user's Clawdbot session if the Wyoming bridge is reachable by untrusted hosts. <br>
Mitigation: Install only on a trusted, firewalled host and restrict the listening address or firewall port 10600 so only Home Assistant can reach it. <br>
Risk: Spoken requests and responses may be retained in the Clawdbot session or logs. <br>
Mitigation: Use a dedicated low-privilege Clawdbot profile, make the .clawdbot mount read-only when possible, and reduce or rotate logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vglafirov/wyoming-clawdbot) <br>
- [Home Assistant Assist](https://www.home-assistant.io/voice_control/) <br>
- [Clawdbot](https://clawd.bot) <br>
- [Wyoming Protocol](https://github.com/rhasspy/wyoming) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime service returns text responses to Home Assistant through the Wyoming Protocol.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
