## Description: <br>
Neural web search and content extraction via SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search the web for documentation, code examples, research papers, company information, and to extract text content from submitted URLs through the SkillBoss API Hub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and submitted URLs are sent to a third-party SkillBoss/HeyBossAI service. <br>
Mitigation: Avoid submitting secrets, private internal URLs, tokens in query strings, confidential research terms, or personal data unless that third-party handling is acceptable. <br>
Risk: The skill requires a sensitive API credential in SKILLBOSS_API_KEY. <br>
Mitigation: Store the key in the environment, restrict access to it, and rotate or revoke it if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/tobeyrebecca/toby-search) <br>
- [Publisher profile](https://clawhub.ai/user/tobeyrebecca) <br>
- [SkillBoss API endpoint used by artifact scripts](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Shell command output from API-backed search and content extraction scripts, typically JSON or text returned by the service.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and jq; submitted search queries and URLs are sent to the SkillBoss/HeyBossAI service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
