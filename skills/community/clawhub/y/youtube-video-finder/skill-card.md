## Description: <br>
Searches multiple online archives to find and recover deleted YouTube videos, metadata, and comments using a video ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upintheairsheep](https://clawhub.ai/user/upintheairsheep) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to check whether a deleted, missing, or private YouTube video has archived video content, metadata, or comments available from online archive services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends YouTube video IDs to a disclosed third-party archive-search API. <br>
Mitigation: Use it only for video IDs that are acceptable to share with the TheTechRobo archive-search service. <br>
Risk: Returned archive links may point to third-party services and recovered content may be sensitive or inappropriate to resurface. <br>
Mitigation: Review archive links and recovered context before sharing them, and avoid using the skill for sensitive or inappropriate content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/upintheairsheep/youtube-video-finder) <br>
- [Find YouTube Video API endpoint](https://findyoutubevideo.thetechrobo.ca/api/v5/{videoid}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summary with recovered archive links, service names, and recovery status notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include direct third-party archive links, metadata-only findings, comment availability, paywall notes, and invalid-ID status messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
