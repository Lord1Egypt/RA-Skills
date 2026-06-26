## Description: <br>
Sniplink is an OpenClaw skill for saving URLs from X, GitHub, and other sites by extracting metadata, categorizing and tagging the link, and storing an approved record. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[almohalhel1408](https://clawhub.ai/user/almohalhel1408) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use Sniplink to quickly save URLs for tools and services, extract useful metadata, categorize and tag entries, and retrieve saved links from an Obsidian vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches metadata for user-provided URLs and stores approved records persistently in an Obsidian vault path that was published with a personal Google Drive location. <br>
Mitigation: Replace the published vault path with the user's chosen folder, confirm each write destination, and avoid submitting private or sensitive URLs unless their metadata should be fetched and stored. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/almohalhel1408/sniplink) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes, summaries, approval prompts, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes approved saved-link records as Obsidian markdown notes and updates an index when configured.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
