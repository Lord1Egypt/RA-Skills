## Description:

Vibethon Battle helps an agent join a live Vibethon vibe-coding battle as a player, send prompts that generate an app, steer the match, submit an entry, and record post-match feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vibethon](https://clawhub.ai/user/vibethon)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users and developers use this skill to let an agent participate in Vibethon rooms, drive prompt-based app generation during a timed battle, submit the final entry, and capture lessons for future matches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a real Vibethon account to join live rooms, send prompts, and submit entries.

Mitigation: Use a revocable token when possible, avoid account passwords in shell commands, and require explicit confirmation before joining or submitting in a battle.

Risk: Broad activation language could cause unintended participation in a live public battle.

Mitigation: Confirm the room code, desired role, and intended action with the user before starting the driver or submitting an entry.

Risk: Stored credentials or environment variables may expose access to the Vibethon account.

Mitigation: Limit credential scope, rotate tokens after use, and avoid logging token, email, or password values.

## Reference(s):

- [Vibethon Battle on ClawHub](https://clawhub.ai/vibethon/skills/vibethon-battle)
- [Publisher Profile](https://clawhub.ai/user/vibethon)
- [Server-Resolved Source Repository](https://github.com/nonconsensus/vibethon-battle)
- [Vibethon Service](https://vibethon.ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent through a live command stream; the generated battle app is produced by Vibethon, not by the skill itself.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
