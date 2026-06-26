## Description: <br>
Fetches X-TechCon technology hot-news items when a supported trigger phrase is present and returns formatted titles, summaries, and links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardtechcon](https://clawhub.ai/user/edwardtechcon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve current technology news from X-TechCon after entering one of the supported trigger phrases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts the fixed external X-TechCon API to retrieve news. <br>
Mitigation: Install only when outbound requests to X-TechCon are acceptable for the deployment environment. <br>
Risk: The Python requests dependency is unpinned. <br>
Mitigation: Pin and review the requests dependency before controlled or repeatable deployments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/edwardtechcon/xtechhotnews) <br>
- [X-TechCon](https://www.x-techcon.com) <br>
- [X-TechCon Hot News API](https://www.x-techcon.com/api/hot_news) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API Calls, guidance] <br>
**Output Format:** [Plain text with numbered news items, summaries, and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a fallback prompt when no supported trigger phrase is present; depends on the fixed X-TechCon hot-news API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
