## Description: <br>
Rolling multi-sport digest skill that tracks current storylines, recent results, upcoming fixtures/events, injuries/availability, and standings across a chosen sports portfolio while keeping a compact context file current. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ds215](https://clawhub.ai/user/ds215) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users configure this skill to produce recurring, audience-specific sports digests for selected teams, leagues, tours, or competitions. It helps maintain continuity between runs by updating a compact rolling context file with current results, upcoming events, availability notes, standings context, and live storylines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The rolling SPORTS_CONTEXT.md file may collect unrelated information or sensitive details if used as a general notes file. <br>
Mitigation: Keep SPORTS_CONTEXT.md limited to sports context and free of secrets, as recommended by the security guidance. <br>
Risk: Sports scores, standings, injuries, and fixtures can be stale or conflicting across sources. <br>
Mitigation: Report only information sourced in the current session, keep uncertainty explicit, and prefer direct current reports when sources conflict. <br>
Risk: Delivery-channel automation or credentials configured outside the skill can introduce operational or security exposure. <br>
Mitigation: Review any separate delivery automation and credentials before deployment. <br>


## Reference(s): <br>
- [SPORTS_CONTEXT_template.md](SPORTS_CONTEXT_template.md) <br>
- [Sports Digest on ClawHub](https://clawhub.ai/ds215/sports-digest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown digest text plus updates to a SPORTS_CONTEXT.md rolling context file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses sourced current-session sports information and keeps the context file compact rather than archival.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
