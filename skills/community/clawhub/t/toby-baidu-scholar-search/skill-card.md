## Description: <br>
Academic Literature Search Tool enables the retrieval of both Chinese and English literature, covering various types of literature such as academic journals, conference papers, and dissertations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to search Chinese and English academic literature through a credentialed SkillBoss API wrapper for Baidu Scholar-style results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and the SkillBoss API key are sent to SkillBoss API Hub rather than directly to Baidu Scholar. <br>
Mitigation: Use a limited, revocable API key and avoid sensitive unpublished research terms unless that data sharing is acceptable. <br>
Risk: The skill depends on a configured SKILLBOSS_API_KEY and curl, so it will fail in environments where either requirement is unavailable. <br>
Mitigation: Confirm the environment variable and curl binary are present before relying on the skill in an agent workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/toby-baidu-scholar-search) <br>
- [Baidu Scholar homepage](https://xueshu.baidu.com/) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls] <br>
**Output Format:** [JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and SKILLBOSS_API_KEY; response results are documented under .result.results.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
