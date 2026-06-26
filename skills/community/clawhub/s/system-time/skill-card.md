## Description: <br>
Provides MCP tools for getting the current system time, returning detailed time information, converting across time zones, and calculating time differences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Qzy05231](https://clawhub.ai/user/Qzy05231) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users can use this skill to answer time-related requests, inspect local and UTC time details, convert common time formats, and calculate elapsed time between two inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: As with any Node package, installing from an untrusted source or using stale dependencies can introduce supply-chain risk. <br>
Mitigation: Install from a trusted ClawHub release and pin or update dependencies for long-term use. <br>
Risk: Time answers depend on the host system clock and the requested timezone. <br>
Mitigation: Verify the host clock and timezone settings before using results in scheduling, audit, or operational workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Qzy05231/system-time) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands] <br>
**Output Format:** [Plain text MCP tool responses with JSON configuration examples and shell commands in documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may vary by local system clock, requested format, and optional timezone.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
