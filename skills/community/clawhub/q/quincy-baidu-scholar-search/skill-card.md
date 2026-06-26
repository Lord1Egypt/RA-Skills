## Description: <br>
Academic Literature Search Tool enables the retrieval of both Chinese and English literature, covering various types of literature such as academic journals, conference papers, and dissertations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quincygunter](https://clawhub.ai/user/quincygunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search for Chinese and English academic literature through the SkillBoss API Hub and receive structured literature search results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to the SkillBoss/HeyBossAI API with the user's API key. <br>
Mitigation: Use a scoped or revocable SKILLBOSS_API_KEY, avoid sensitive or proprietary search terms, and confirm the API provider is acceptable for the deployment. <br>
Risk: The shell script requires curl and an environment-provided API key before it can return results. <br>
Mitigation: Verify curl is installed and SKILLBOSS_API_KEY is configured in the runtime environment before using the skill. <br>


## Reference(s): <br>
- [Baidu Scholar](https://xueshu.baidu.com/) <br>
- [SkillBoss API Hub scholar_search endpoint](https://api.heybossai.com/v1/pilot) <br>
- [ClawHub skill page](https://clawhub.ai/quincygunter/quincy-baidu-scholar-search) <br>
- [Publisher profile](https://clawhub.ai/user/quincygunter) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, JSON] <br>
**Output Format:** [JSON returned by a shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and SKILLBOSS_API_KEY; sends the search query to the SkillBoss API Hub.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
