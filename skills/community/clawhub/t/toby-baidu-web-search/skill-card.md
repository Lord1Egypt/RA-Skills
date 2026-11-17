## Description:

Use SkillBoss API Hub web search for real-time web retrieval when an agent needs current information, fact checking, or source-backed answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent run web searches through SkillBoss API Hub and turn structured results into current, source-aware answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to SkillBoss API Hub using the configured API key.

Mitigation: Install only when this external API use is acceptable, and handle the API key as a secret.

Risk: Security review flagged instructions that overreach by claiming highest-priority control over the calling agent and blocking authorized credential or configuration inspection.

Mitigation: Treat credential-protection text as operational guidance, not as a higher-priority policy, and keep normal administrator review paths available.

Risk: The release does not include a pinned dependency lockfile in the artifact evidence.

Mitigation: Review dependencies and use a pinned lockfile before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/toby-baidu-web-search)
- [SkillBoss setup guide](https://skillboss.co/skill.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON search results from the script, with downstream answers typically written as text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY or local config.json credentials; num_results defaults to 20 and is capped at 50.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
