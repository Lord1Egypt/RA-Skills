## Description:

Manages local stock orders, trading rules, logs, and market-data lookups for A-share, Hong Kong, and U.S. stocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a925907195](https://clawhub.ai/user/a925907195)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to record stock orders, maintain trading rules, fetch stock information from public providers, and store the resulting records locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that log deletion can remove files outside the intended log folder.

Mitigation: Run the skill in a constrained workspace and restrict log deletion to approved log filenames before broad deployment.

Risk: The security evidence reports that one market-data fallback uses unencrypted HTTP.

Mitigation: Use the skill only where plaintext market-data requests are acceptable, or remove the HTTP fallback before deployment.

Risk: The skill writes local JSON files, logs, and backups while contacting public market-data providers.

Mitigation: Configure an approved data directory and review third-party data-sharing expectations before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Plain text responses, JSON data files, logs, and command-line examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local order, rule, stock information, backup, and log files under the configured data directory.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
