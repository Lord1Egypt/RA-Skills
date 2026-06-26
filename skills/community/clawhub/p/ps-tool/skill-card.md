## Description: <br>
Display information about active processes for monitoring running programs, checking resource usage, and system diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and support engineers use this skill to inspect active Linux processes and support routine system diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Process listings can reveal command-line arguments, including usernames, project paths, tokens, or other local details. <br>
Mitigation: Review output before sharing it and avoid running the skill in contexts where process command lines contain sensitive values. <br>
Risk: The artifact documents filtering and sorting options that are not implemented by the bundled script. <br>
Mitigation: Treat the skill as a basic process listing helper unless the implementation is updated to support the documented options. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text process listings and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Process command lines may expose local usernames, paths, or secrets passed as command-line arguments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
