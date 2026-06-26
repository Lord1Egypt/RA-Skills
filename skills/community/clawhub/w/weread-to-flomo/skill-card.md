## Description: <br>
Sync WeRead (微信读书) highlights and notes into flomo with incremental deduplication and configurable sync scope. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericxie777](https://clawhub.ai/user/ericxie777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to sync locally exported WeRead annotations into flomo, choosing today's notes, a specific date, or a full migration while avoiding duplicate pushes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A live sync can post unintended or duplicate WeRead notes to the configured flomo webhook. <br>
Mitigation: Run --dry-run first, verify the webhook value, and prefer today or date mode before using all mode. <br>
Risk: Users may provide a WeRead cookie even though the included script processes already-exported Markdown files. <br>
Mitigation: Do not provide or store a WeRead session cookie for this skill unless the maintainer documents why it is required. <br>


## Reference(s): <br>
- [Formatting](references/formatting.md) <br>
- [Publishing notes](references/publishing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration flags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run mode, local state tracking, configurable tag prefixes, and today/date/all sync scopes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
