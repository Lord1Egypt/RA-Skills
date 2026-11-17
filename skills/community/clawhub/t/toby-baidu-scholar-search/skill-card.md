## Description:

Academic Literature Search Tool enables the retrieval of both Chinese and English literature, covering various types of literature such as academic journals, conference papers, and dissertations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and researchers use this skill to submit academic literature search keywords and retrieve Chinese and English scholarly literature results through the SkillBoss API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and the SkillBoss API key are sent to the SkillBoss API, and sensitive research terms may be exposed to that service.

Mitigation: Avoid highly sensitive or confidential queries and install only when sending search terms to SkillBoss is acceptable.

Risk: The shell script interpolates the query into JSON without safe JSON encoding.

Mitigation: Prefer a fixed release that JSON-encodes the query before sending it, especially for user-provided or untrusted search strings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/toby-baidu-scholar-search)
- [Baidu Scholar](https://xueshu.baidu.com/)
- [SkillBoss setup guide](https://skillboss.co/skill.md)
- [SkillBoss API endpoint](https://api.skillboss.co/v1/pilot)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON response from a shell-based API call, with setup and usage guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and SKILLBOSS_API_KEY; expected results are under .result.results.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
