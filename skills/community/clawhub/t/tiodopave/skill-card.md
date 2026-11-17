## Description:

Fetches recent, clean jokes from Reddit's r/tiodopave community and returns one joke while avoiding immediate repetition and NSFW content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runawaydevil](https://clawhub.ai/user/runawaydevil)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to retrieve a recent Portuguese joke from r/tiodopave for conversation or entertainment. It is useful when the agent should relay Reddit-sourced jokes rather than generate jokes itself.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Reddit and prints untrusted user-generated Reddit posts.

Mitigation: Treat returned jokes as untrusted external content and review them before publishing, logging, or relaying in sensitive contexts.

Risk: The package uses fixed shared temporary file paths that could be abused on shared systems.

Mitigation: Store state in a private user-owned directory or use securely created temporary files before routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runawaydevil/skills/tiodopave)
- [Reddit r/tiodopave](https://www.reddit.com/r/tiodopave)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text joke with optional title and body]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live Reddit content and may return an error message if Reddit is unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
