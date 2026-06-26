## Description: <br>
Convert timezones, resolve natural language times ("next Tuesday at 2pm"), compute durations, and adjust timestamps with DST awareness. No credentials needed; all tools run fully offline after one-time binary install. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billylui](https://clawhub.ai/user/billylui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to resolve current temporal context, natural-language datetime expressions, timezone conversions, durations, and DST-aware timestamp adjustments without credentials or runtime network calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Initial installation uses an npm package that installs a native binary. <br>
Mitigation: Inspect the npm package before installation and independently verify the release checksum before first use. <br>
Risk: A misconfigured or stale local timezone setting can produce misleading datetime interpretations. <br>
Mitigation: Call get_temporal_context before time-dependent work and confirm the configured timezone when results affect scheduling or deadlines. <br>
Risk: Runtime containment depends on the chosen launch path. <br>
Mitigation: Use the documented Docker mode with networking disabled when stronger isolation is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/billylui/temporal-cortex-datetime) <br>
- [Temporal Cortex homepage](https://temporal-cortex.com) <br>
- [Temporal Cortex skills repository](https://github.com/temporal-cortex/skills) <br>
- [Temporal Cortex MCP package](https://www.npmjs.com/package/@temporal-cortex/cortex-mcp) <br>
- [Datetime Tools Reference](references/DATETIME-TOOLS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with datetime tool results, configuration snippets, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Datetime outputs use RFC 3339 timestamps, IANA timezones, UTC offsets, and DST-aware local time fields where applicable.] <br>

## Skill Version(s): <br>
0.9.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
