## Description: <br>
Handle messages in a Discord sleep-tracking channel by grounding all sleep logging and summaries on the real sleep tracker and source Discord metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cdmichaelb](https://clawhub.ai/user/cdmichaelb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to maintain a Discord-based sleep log, including adding events, correcting or deleting the latest entry, and rendering the current log from stored records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sleep history and Discord metadata are stored in local workspace files. <br>
Mitigation: Install only where local storage of this data is acceptable, use a dedicated sleep-tracking channel, and restrict access to the workspace. <br>
Risk: Incorrect or missing time context can produce inaccurate sleep records. <br>
Mitigation: Set SLEEP_TIMEZONE explicitly and pass source Discord message timestamps unless the user provides an explicit time. <br>
Risk: Correction and deletion requests can change the local sleep log. <br>
Mitigation: Treat correction or deletion as a command only when the user intent is clear, and ask a short clarifying question when it is ambiguous. <br>


## Reference(s): <br>
- [Sleep Channel Skill Page](https://clawhub.ai/cdmichaelb/sleep-channel) <br>
- [Sleep Channel Rules](references/CHANNEL_RULES.md) <br>
- [Sleep Tracking System](references/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON tracker responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local CSV and JSON state files under the configured workspace.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
