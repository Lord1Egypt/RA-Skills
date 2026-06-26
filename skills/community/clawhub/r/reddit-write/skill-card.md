## Description: <br>
Drafts Reddit posts and comments in Luka's voice from research findings, subreddit rules, and writing templates for manual review before posting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lknezic](https://clawhub.ai/user/lknezic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Operators supporting Luka use this skill to turn prior Reddit research into draft posts and comments that match his trading voice and subreddit constraints. The drafts are saved for Luka's manual review and posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill tells the agent to imitate Luka's voice and avoid being flagged as AI-written. <br>
Mitigation: Use only with Luka's authorization, remove AI-detection-evasion instructions, and keep manual review mandatory. <br>
Risk: Drafts may mention QuantWheel in Reddit communities with disclosure or external-link restrictions. <br>
Mitigation: Verify subreddit rules and affiliation disclosure before any QuantWheel mention, and require Luka's approval before posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lknezic/reddit-write) <br>
- [Post templates](artifact/ref-templates.md) <br>
- [Luka's voice reference](artifact/ref-voice.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown draft files with frontmatter and Reddit-ready post or comment text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Drafts require human review before posting and are not auto-posted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
