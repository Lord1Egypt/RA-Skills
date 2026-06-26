## Description: <br>
Looks up standard-edition Sanguosha hero skills from public sources and returns concise skill names and descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cpufreestyle](https://clawhub.ai/user/cpufreestyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and game-reference agents use this skill to answer natural-language questions about standard-edition Sanguosha hero abilities. It identifies a requested hero, searches public references, and summarizes the relevant skill names and descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ambiguous character-name questions could trigger this skill unexpectedly. <br>
Mitigation: Confirm the user is asking about a Sanguosha standard-edition hero when the request is unclear. <br>
Risk: Lookup prompts may be sent through web search. <br>
Mitigation: Avoid including private information in hero-skill lookup prompts. <br>
Risk: The skill is limited to standard-edition heroes. <br>
Mitigation: Tell users when a requested hero appears to come from an expansion set and suggest checking a complete Sanguosha reference. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cpufreestyle/sanguosha-hero) <br>
- [Sanguosha Wiki](https://wiki.sanguosha.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with hero names, skill names, and skill descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask a follow-up question when the user does not specify a hero; limited to standard-edition heroes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
