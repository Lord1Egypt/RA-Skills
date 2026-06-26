## Description: <br>
Helps identify coordinated social trust manipulation in agent marketplaces by detecting reputation gaming through sockpuppet networks, coordinated upvoting, and manufactured community signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, marketplace users, and moderators use this skill to assess whether trust signals for a skill, publisher, or group of skills appear organic or manipulated before relying on reputation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manipulation verdicts could affect publisher reputation or moderation decisions. <br>
Mitigation: Treat SUSPICIOUS, COORDINATED, and MANUFACTURED results as investigative leads and verify the underlying evidence before reporting a publisher or taking moderation action. <br>
Risk: Limited marketplace metadata can reduce detection confidence. <br>
Mitigation: State which evidence dimensions are unavailable and limit conclusions to observable velocity and review-text signals when account, voting, or install data is missing. <br>
Risk: Legitimate launches, press coverage, or featured placement can resemble coordinated burst engagement. <br>
Mitigation: Compare suspicious bursts against launch context, marketplace promotion history, account diversity, and platform-level data before concluding manipulation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/andyxinweiminicloud/social-trust-manipulation-detector) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/andyxinweiminicloud) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown manipulation detection report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports engagement velocity, account cohort fingerprints, utility correlation, coordination indicators, review authenticity, and an AUTHENTIC/SUSPICIOUS/COORDINATED/MANUFACTURED verdict.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
