## Description: <br>
Provides Bilibili CLI guidance for retrieving video details, subtitles, AI summaries, comments, related videos, audio segments, user data, search results, rankings, feeds, collections, history, and account interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to ask an agent for Bilibili data retrieval, audio extraction, structured YAML or JSON outputs, and authenticated account actions through bilibili-cli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use saved or browser login sessions, which may expose private account data without the user noticing. <br>
Mitigation: Prefer QR login, review credential handling before installation, and require explicit user approval before reading private account areas such as favorites, watch-later, history, feeds, or following lists. <br>
Risk: The skill includes account-changing actions such as like, coin, triple, and unfollow. <br>
Mitigation: Require the agent to ask for explicit confirmation before any account-changing command and show the target video or user identifier before execution. <br>
Risk: The skill depends on bilibili-cli behavior and package integrity. <br>
Mitigation: Verify the bilibili-cli package source and version before installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianheihei002/yq-bilibili-skill) <br>
- [Publisher profile](https://clawhub.ai/user/tianheihei002) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and references to YAML or JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to create audio files or structured YAML/JSON results when bilibili-cli is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
