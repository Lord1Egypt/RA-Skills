## Description:

Baidu Scholar Search retrieves Chinese and English academic literature, including journal articles, conference papers, and dissertations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and agents use this skill to submit academic search keywords through SkillBoss API Hub and retrieve structured literature results across Chinese and English sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords are sent to a third-party API using an environment API key.

Mitigation: Use only with queries appropriate for that service, avoid sensitive or unpublished research topics unless the service is trusted, and scope or rotate the API key according to local policy.

Risk: The request body is assembled by interpolating the query into JSON without escaping.

Mitigation: Review or patch the request construction to JSON-escape user input before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quincygunter/skills/quincy-baidu-scholar-search)
- [Baidu Scholar](https://xueshu.baidu.com/)
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and SKILLBOSS_API_KEY; search keywords are sent to SkillBoss/HeyBossAI.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
