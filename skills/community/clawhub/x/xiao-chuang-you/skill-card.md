## Description:

Xiao Chuang You is a Chinese-language new-Chinese lifestyle aesthetics guide that answers or routes questions about weather, pets, wellness, music, literature, clothing, crafts, photography, gardening, objects, seasons, travel, and emotions in a gentle classical style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zcr3344](https://clawhub.ai/user/zcr3344)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent skill for Chinese-language lifestyle recommendations, seasonal suggestions, and aesthetic guidance across daily living domains. Agents can also use it to route domain-specific requests to companion subskills or fall back to bundled reference material when those subskills are unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks to remember location, preference, and health-adjacent personalization details in local memory.

Mitigation: Install only if this local personalization is acceptable; avoid sharing medical details, diagnoses, medications, or highly private location information, and review or delete /workspace/MEMORY.md and memory summaries as needed.

Risk: The skill declares an automatic monthly memory-checking job.

Mitigation: Verify any scheduled cron task before relying on it, and remove it if unwanted.

Risk: Time-sensitive recommendations may use live search, weather data, or third-party links.

Mitigation: Verify external links, weather results, and current-event recommendations before acting on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zcr3344/skills/xiao-chuang-you)
- [Reference Index](references/INDEX.md)
- [Capabilities Matrix](references/capabilities.md)
- [Conversation Flow](references/conversation-flow.md)
- [Data Declaration](references/data-declaration.md)
- [Response Guidelines](references/guidelines.md)
- [Weather System](references/weather.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown conversational responses with recommendations, short lists, tables, and links when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include routed subskill guidance, fallback answers from bundled references, local-memory personalization notes, and source labels for weather responses.]

## Skill Version(s):

2.2.1 (source: server release evidence and target metadata; artifact _meta.json reports 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
