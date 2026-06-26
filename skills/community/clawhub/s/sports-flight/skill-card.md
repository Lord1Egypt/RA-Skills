## Description: <br>
sports-flight helps agents find sports-event and game-day flight options through the FlyAI CLI and present real-time booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users planning travel for sports events use this skill to collect flight search parameters, run the FlyAI CLI, and compare bookable options. Agents use it to produce concise travel guidance with booking links rather than relying on static travel knowledge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires installing and running the external FlyAI npm CLI globally. <br>
Mitigation: Install only in environments where that external dependency is approved, and review the package before use. <br>
Risk: Travel-search details are sent through the external FlyAI provider. <br>
Mitigation: Avoid submitting sensitive travel details unless the provider and data handling are acceptable for the user or organization. <br>
Risk: Flight prices, availability, booking terms, and links can change after results are returned. <br>
Mitigation: Review booking links, prices, and terms directly before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/sports-flight) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, inline shell commands, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FlyAI CLI results; booking options should include detailUrl links when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
