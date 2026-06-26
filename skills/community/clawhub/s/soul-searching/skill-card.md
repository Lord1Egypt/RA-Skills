## Description: <br>
Soul Searching helps OpenClaw agents browse, install, switch, and manage SOUL.md personality files from the soulsearching.ai directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stirman](https://clawhub.ai/user/stirman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover SOUL.md personality files, install them into an OpenClaw local cache, and activate or switch the workspace SOUL.md when changing agent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote SOUL.md files can change agent behavior after installation or activation. <br>
Mitigation: Review downloaded SOUL.md content before activation and install only from trusted soulsearching.ai catalog entries. <br>
Risk: The switch and install --activate commands can replace the workspace SOUL.md. <br>
Mitigation: Keep the automatic SOUL.md.bak backup and confirm the target workspace before switching souls. <br>
Risk: Unusual soul IDs could be unsafe if they include path traversal or slash-like values. <br>
Mitigation: Use normal catalog IDs only and avoid IDs containing slashes, parent-directory segments, or other unexpected path characters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stirman/soul-searching) <br>
- [Soul Searching directory](https://soulsearching.ai) <br>
- [Soul catalog endpoint](https://soulsearching.ai/souls.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads remote SOUL.md content to ~/.openclaw/souls and can copy an installed soul to the workspace SOUL.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
