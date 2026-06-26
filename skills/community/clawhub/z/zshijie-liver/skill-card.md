## Description: <br>
Resolves Z视介 live channel requests or common program aliases to a supported channel, opens the corresponding live page, and returns a short Markdown watch card. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jkbwfi](https://clawhub.ai/user/jkbwfi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to open supported Z视介 live TV channels by channel name, cid, or common aliases such as 跑男 or 奔跑吧. The skill maps the request to a live channel and returns a concise Markdown card with a clickable watch link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper may open a fixed Z视介 live page in the user's browser. <br>
Mitigation: Use --no-open or request a link-only response when automatic browser navigation is not wanted. <br>
Risk: Short aliases may resolve to a supported live channel without asking for clarification. <br>
Mitigation: Ask the user to confirm when a channel request is ambiguous or unsupported, and rely on the bundled channel map instead of guessing. <br>


## Reference(s): <br>
- [Z视介 Channel Map](references/channel_map.md) <br>
- [Zshijie Liver on ClawHub](https://clawhub.ai/jkbwfi/zshijie-liver) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, JSON, text, shell commands, guidance] <br>
**Output Format:** [Markdown card with a clickable live-link by default; optional JSON or URL-only text from the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open the resolved live page in the default browser unless the agent uses --no-open.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
