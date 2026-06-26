## Description: <br>
查询上海落户公示信息，包括人才引进公示和居转户公示。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luduoxin](https://clawhub.ai/user/luduoxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find public Shanghai settlement notice pages for talent-introduction and residence-permit-to-household-registration processes, then review the official links or printed summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public sh-italent.com pages and may open browser tabs automatically. <br>
Mitigation: Run with --no-browser when only printed results are needed, and review the official URLs before relying on the results. <br>
Risk: Company and person query options are limited and may not filter results as expected. <br>
Mitigation: Treat company or person-specific results as preliminary, then open the official notice pages and verify names or organizations manually. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luduoxin/shanghai-luohu) <br>
- [Shanghai International Talent official site](https://www.sh-italent.com/) <br>
- [Shanghai settlement notice list](https://www.sh-italent.com/News/NewsList.aspx?TagID=5696) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Console text with official notice URLs; may open browser tabs unless --no-browser is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public web pages at runtime and does not require credentials.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
