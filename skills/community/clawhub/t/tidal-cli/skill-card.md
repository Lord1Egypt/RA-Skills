## Description: <br>
Control Tidal music streaming from the terminal for catalog search, playlist and library management, playback, recommendations, and profile lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucaperret](https://clawhub.ai/user/lucaperret) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate tidal-cli for Tidal search, playback, playlist, library, recommendation, and account profile workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete Tidal account content, including playlists, tracks, and library favorites. <br>
Mitigation: Require explicit user confirmation before delete, rename, remove, favorite, or unfavorite actions, and present the exact target item before execution. <br>
Risk: Ambiguous music requests could cause the agent to act on the wrong track, artist, album, or playlist. <br>
Mitigation: Resolve ambiguous requests with a clarification step or show candidate matches before taking account-changing actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lucaperret/skills/tidal-cli) <br>
- [npm package @lucaperret/tidal-cli](https://www.npmjs.com/package/@lucaperret/tidal-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommends --json for programmatic CLI output; underlying command results may include Tidal account and catalog data.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
