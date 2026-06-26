## Description: <br>
Skill Tracker records Python and Node.js skill usage, success rates, timing, and rankings in local files for usage analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiyst1982](https://clawhub.ai/user/aiyst1982) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to instrument Python or Node.js skills, collect local usage statistics, and review reports that show call counts, success rates, failures, and timing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local logs may include user, session, and error metadata. <br>
Mitigation: Protect or periodically delete the data directory, configure retention, and avoid passing secrets, tokens, personal data, or raw exception text into context or error fields. <br>
Risk: The tracker records usage history for any skills integrated with it. <br>
Mitigation: Use it only with skills whose activity you intentionally want recorded, and disable raw logging or remove the tracker where local activity history is not appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiyst1982/skill-tracker-aiyst) <br>
- [Publisher profile](https://clawhub.ai/user/aiyst1982) <br>
- [README](artifact/README.md) <br>
- [CHANGELOG](artifact/CHANGELOG.md) <br>
- [Configuration example](artifact/config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, local JSON/JSONL usage data, and Python or Node.js integration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 according to ClawHub metadata; supports Linux, macOS, and Windows.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
