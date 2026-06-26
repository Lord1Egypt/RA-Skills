## Description: <br>
Query Last.fm listening data, show now playing, sync scrobble history to local DB, and deploy a personal "now playing" web dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poiley](https://clawhub.ai/user/poiley) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and engineers use this skill to query Last.fm listening data, manage local scrobble history, and set up a personal now-playing dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release package includes unrelated personal workspace files and high-privilege automation instructions. <br>
Mitigation: Review the full package before installation and republish a scoped release containing only the Last.fm dashboard skill files. <br>
Risk: The release security summary reports exposed credentials in the package. <br>
Mitigation: Remove exposed credentials from the package, rotate affected secrets, and verify the cleaned release before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/poiley/whatisxlistening-to) <br>
- [Last.fm API account creation](https://www.last.fm/api/account/create) <br>
- [Live dashboard demo](https://whatisbenlistening.to) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and deployment guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Last.fm API setup steps, local SQLite sync guidance, Docker commands, and Kubernetes configuration guidance.] <br>

## Skill Version(s): <br>
1.3.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
