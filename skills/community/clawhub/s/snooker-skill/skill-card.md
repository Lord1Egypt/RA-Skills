## Description:

Look up snooker rankings, results, player profiles, live matches and head-to-head records via api.snooker.org.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rgstephens](https://clawhub.ai/user/rgstephens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and snooker-focused agents use this skill to retrieve professional tour rankings, results, schedules, live matches, player profiles, tournament details, and head-to-head records from api.snooker.org.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional setup command can save the Snooker API key locally in plaintext.

Mitigation: Prefer setting SNOOKER_API_KEY in the runtime environment and avoid using setup unless local plaintext storage is acceptable.

Risk: The skill sends authenticated requests to api.snooker.org.

Mitigation: Install only in environments where outbound access to api.snooker.org and use of a Snooker API key are acceptable.

## Reference(s):

- [Snooker API](https://api.snooker.org/)
- [ClawHub Skill Page](https://clawhub.ai/rgstephens/skills/snooker-skill)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a SNOOKER_API_KEY for api.snooker.org.]

## Skill Version(s):

0.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
