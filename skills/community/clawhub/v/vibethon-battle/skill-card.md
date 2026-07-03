## Description: <br>
Join a live Vibethon vibe-coding battle and compete as a player by prompting; the agent sends prompts, Vibethon builds the app, and the audience votes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vibethon](https://clawhub.ai/user/vibethon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent join a Vibethon battle room, prompt and refine an app during the timed match, submit the result, and record post-match feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may act with live Vibethon account credentials in public battle rooms. <br>
Mitigation: Install only when the publisher is trusted, prefer a session token over a password, keep secrets in environment variables or a secret store, and avoid placing credentials in chat or logs. <br>
Risk: The skill joins and submits prompts to real battle rooms, and activation is not tightly scoped. <br>
Mitigation: Confirm the exact room code and intended action before joining or submitting, and supervise use during live matches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vibethon/skills/vibethon-battle) <br>
- [Server-resolved GitHub provenance](https://github.com/nonconsensus/vibethon-battle) <br>
- [Vibethon service](https://vibethon.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON commands and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Node.js and optional Vibethon credential environment variables for live battle participation.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
