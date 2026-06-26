## Description: <br>
Plans intentionally low-comfort novelty travel itineraries using FlyAI travel search, with booking links, humorous commentary, trip interaction, and post-trip markdown content generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catshcrozhang](https://clawhub.ai/user/catshcrozhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to generate intentionally rough, humorous travel challenge plans that can include real-time transport, hotel, and attraction searches through FlyAI. The skill also supports in-trip commentary and produces markdown trip diaries, reversal reports, short-video titles, scripts, and share copy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can surface real third-party booking links for travel purchases. <br>
Mitigation: Review destination, dates, prices, refund terms, merchant domain, and booking details before clicking through or paying. <br>
Risk: The skill depends on the third-party FlyAI CLI for live travel search. <br>
Mitigation: Install and use the FlyAI CLI only if the operator trusts that dependency and its returned travel data. <br>
Risk: Randomized or intentionally low-comfort travel suggestions may not match user constraints. <br>
Mitigation: Confirm budget, dates, health constraints, and explicit user approval before acting on any proposed itinerary. <br>


## Reference(s): <br>
- [Detailed reference document](references/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/catshcrozhang/worst-travel-challenge) <br>
- [FlyAI](https://flyai.open.fliggy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with travel options, booking links, commentary, and generated script content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include real third-party Fliggy booking links and FlyAI CLI commands.] <br>

## Skill Version(s): <br>
1.1.5 (source: release evidence; artifact frontmatter reports 1.1.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
