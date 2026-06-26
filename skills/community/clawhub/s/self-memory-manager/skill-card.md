## Description: <br>
Self Memory Manager helps Claude monitor context usage, archive important work notes, summarize progress, and maintain a local memory folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyk234](https://clawhub.ai/user/hyk234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users use this skill to keep long-running Claude sessions organized by prompting context archiving, saving task progress, and retrieving prior notes from a local workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to save account or API details and copy an OpenClaw configuration file into a desktop notes folder, which can expose secrets or sensitive configuration. <br>
Mitigation: Remove the config-copy command, prohibit saving secrets, tokens, account details, and raw configuration files, and require explicit approval before writing to or searching the memory folder. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and folder structure examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local-memory workflow guidance and may propose file reads or writes in the configured notes folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
