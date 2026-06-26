## Description: <br>
Use SkillBoss API Hub web search for real-time web retrieval when users need current web information, fact checks, authoritative sources, or lookup of recent events, people, products, and places. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to run live web searches through SkillBoss API Hub and turn structured search results into source-based answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and the configured API key are sent to SkillBoss when live lookup is used. <br>
Mitigation: Install only when SkillBoss is trusted, configure the key through private skill settings where possible, and avoid searching for secrets or sensitive personal data. <br>
Risk: Broad auto-activation wording may cause the skill to be used for queries that do not need live web lookup. <br>
Mitigation: Use the skill only when current web retrieval, fact checking, or source discovery is actually needed. <br>
Risk: Search results can be stale, incomplete, or misleading. <br>
Mitigation: Have the calling agent cite and compare returned sources before presenting conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/toby-baidu-web-search) <br>
- [Publisher profile](https://clawhub.ai/user/tobeyrebecca) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [SkillBoss API endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results from the script, followed by human-facing text or Markdown answers composed by the calling agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY or a local apiKey configuration; search results include title, URL, snippet, total count, query, and engine.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
