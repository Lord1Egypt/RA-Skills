## Description: <br>
Analyze repository changes from the last release to the current revision and recommend the correct semantic version bump. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nick2bad4u](https://clawhub.ai/user/nick2bad4u) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release maintainers use this skill to inspect repository changes, package metadata, and public contract evidence before deciding whether the next release should be patch, minor, or major. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Release recommendations can be wrong when tags, generated API documentation, package metadata, or public contract evidence are incomplete. <br>
Mitigation: Review the stated confidence and residual risk, collect missing evidence, and verify the recommendation against actual diffs before tagging or publishing. <br>
Risk: The skill may suggest shell commands to collect release evidence. <br>
Mitigation: Review commands before running them and keep execution scoped to the repository being analyzed. <br>


## Reference(s): <br>
- [Source repository](https://github.com/Nick2bad4u/semver-release-recommender) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown recommendation with evidence summary, rationale, checks, and residual risk] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a semver bump recommendation, confidence level, release range, current and next versions, and commands used to collect evidence.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
