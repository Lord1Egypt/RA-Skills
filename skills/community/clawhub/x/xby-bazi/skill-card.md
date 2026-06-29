## Description: <br>
Xby Bazi helps an agent retrieve BaZi chart details, matching solar times, and Chinese calendar information through the XiaoBenYang API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to route BaZi, solar/lunar date, gender, and calendar queries to the XiaoBenYang API and summarize the returned JSON for end users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BaZi query inputs are sent to xiaobenyang.com through a third-party API. <br>
Mitigation: Use the skill only when sharing those inputs with the XiaoBenYang service is acceptable. <br>
Risk: The required XBY_APIKEY can be stored locally in a plaintext .env file. <br>
Mitigation: Remove the key from .env when uninstalling the skill or when credential retention is no longer desired. <br>


## Reference(s): <br>
- [Xby Bazi on ClawHub](https://clawhub.ai/cainingnk/xby-bazi) <br>
- [Publisher profile](https://clawhub.ai/user/cainingnk) <br>
- [XiaoBenYang](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls, guidance] <br>
**Output Format:** [Markdown or text summaries of JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY_APIKEY value before API calls can be made.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
