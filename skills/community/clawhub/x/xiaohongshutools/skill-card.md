## Description: <br>
XiaoHongShu (Little Red Book) data collection and interaction toolkit for searching and scraping notes, retrieving user profiles, extracting comments and engagement data, fetching feeds, and optionally following users or liking posts with an authenticated session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChocomintX](https://clawhub.ai/user/ChocomintX) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to automate XiaoHongShu data collection workflows, including note search, profile lookup, comment extraction, and feed retrieval. Authenticated use can also perform account actions such as following users, liking posts, and interacting with comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated workflows can act as the user's XiaoHongShu account. <br>
Mitigation: Use a dedicated low-impact account, limit permissions where possible, and avoid sharing web_session cookies in prompts, logs, or team channels. <br>
Risk: The security evidence flags account-state changes, engagement-manipulation behavior, session-cookie logging, and unsafe config execution. <br>
Mitigation: Review or remove mutation APIs, read-count metrics workflows, cookie logging, and the eval-based config parser before production use. <br>
Risk: Automation may trigger platform security controls, rate limits, or account enforcement. <br>
Mitigation: Use only legitimate workflows, keep request rates conservative, and stop automation when XiaoHongShu returns security, permission, or ban-related responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChocomintX/xiaohongshutools) <br>
- [RedCrack](https://github.com/Cialle/RedCrack) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and API response handling notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide use of proxies, web_session cookies, XiaoHongShu note identifiers, and asynchronous Python API calls.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
