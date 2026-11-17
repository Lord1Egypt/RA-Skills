## Description:

Neural web search and content extraction via SkillBoss API Hub. Requires SKILLBOSS_API_KEY. Use for finding documentation, code examples, research papers, or company info.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and other external users can use this skill to search the web, find code or documentation context, and extract text from supplied URLs through the SkillBoss API Hub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, requested URLs, and the SkillBoss API token are sent to the HeyBossAI/SkillBoss API.

Mitigation: Avoid private internal URLs, credential-bearing links, or sensitive queries unless third-party processing is acceptable for the deployment environment.

Risk: Search and extracted-content responses may be incomplete, stale, or unsuitable for direct use without review.

Mitigation: Review returned content and source relevance before using it in downstream decisions, code, or documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/toby-search)
- [HeyBossAI SkillBoss API endpoint](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell command guidance with JSON API responses from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends search queries or requested URLs to a third-party API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
