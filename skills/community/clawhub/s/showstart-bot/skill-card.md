## Description: <br>
Showstart Skills helps agents query Showstart event information, including event details and searches by keyword, city, category, style, artist, venue, or nearby coordinates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[austin-am](https://clawhub.ai/user/austin-am) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up Showstart event details and search live listings by keyword, city, category, style, artist, venue, or nearby coordinates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and nearby-search coordinates are sent to the Showstart service, and the security evidence flags optional nearby searches as a privacy concern. <br>
Mitigation: Avoid exact home or work coordinates, avoid sensitive search terms, and prefer the documented HTTPS endpoint before sharing precise location data. <br>


## Reference(s): <br>
- [Showstart Skill API Documentation](references/api_docs.md) <br>
- [Showstart Skill Page](https://clawhub.ai/austin-am/showstart-bot) <br>
- [Showstart API Endpoint](https://skill.showstart.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and Showstart API result data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include paginated event data, formatted event summaries, and cached API responses.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
