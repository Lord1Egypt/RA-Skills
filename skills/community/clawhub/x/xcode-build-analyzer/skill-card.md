## Description:

Analyze Xcode build logs for timing, warnings, errors, slow compiles, and build history from DerivedData.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexissan](https://clawhub.ai/user/alexissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill on macOS to inspect Xcode DerivedData build records, summarize build history, find warnings and errors, identify slow build steps, and compare IDE and CLI build activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports that two documented all-project summary command recipes can execute attacker-controlled Python if a crafted DerivedData directory exists.

Mitigation: Review those command recipes before use, avoid running them on systems where untrusted users or tools can create DerivedData entries, and pass directory names to Python as data through argv or environment variables instead of embedding them in Python source.

Risk: The skill reads Xcode DerivedData and may require broader file access depending on the agent process.

Mitigation: Grant Full Disk Access only when needed and prefer the narrowest local permissions that allow the requested build-log inspection.

Risk: The skill includes a DerivedData cleanup recipe that deletes build cache contents when explicitly requested.

Mitigation: Confirm the target path and printed disk usage with the user before running any deletion command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexissan/skills/xcode-build-analyzer)
- [Publisher profile](https://clawhub.ai/user/alexissan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and terminal-oriented summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only analysis guidance for local Xcode DerivedData; some commands require macOS, Xcode build data, plutil, gunzip, and sqlite3.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
