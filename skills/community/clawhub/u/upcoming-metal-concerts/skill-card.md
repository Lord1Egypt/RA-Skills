## Description: <br>
Collect upcoming metal concerts and festivals by country using concerts-metal.com. Use when the user asks about upcoming metal shows, gigs, or festivals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PatFitzner](https://clawhub.ai/user/PatFitzner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect upcoming metal concert and festival listings for a selected country, store the results locally, and identify previously seen future events that may have been cancelled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts concerts-metal.com and depends on the site's availability and page structure. <br>
Mitigation: Run it only when network access to concerts-metal.com is acceptable, and review collected results before relying on them. <br>
Risk: The skill keeps local configuration and accumulated concert results on disk. <br>
Mitigation: Review or delete skill-config.json and data/concerts.json to reset stored country, lookahead, and concert data. <br>


## Reference(s): <br>
- [Upcoming Metal Concerts on ClawHub](https://clawhub.ai/PatFitzner/upcoming-metal-concerts) <br>
- [concerts-metal.com broadcast pages](https://broadcast.concerts-metal.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, JSON files] <br>
**Output Format:** [Markdown guidance with shell commands and local JSON data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates skill-config.json and data/concerts.json; contacts concerts-metal.com and requires python3.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
