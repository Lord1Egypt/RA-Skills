## Description: <br>
Plan the perfect 2-day weekend escape to nearby destinations by using flyai CLI results for flights, hotels, attractions, and booking-linked itinerary guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers use this skill to plan short weekend getaways, compare real-time flight and hotel options, find attractions, and receive concise Markdown recommendations with booking links. Agents use it when the user asks for a weekend trip, short break, two-day getaway, or equivalent Chinese-language request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and execute a global flyai CLI package before planning travel. <br>
Mitigation: Review and approve the npm package before installation, and run the skill in an environment where global package installation is acceptable. <br>
Risk: Travel details may be sent to flyai or Fliggy during real-time search and booking workflows. <br>
Mitigation: Avoid entering passport, payment, identity, or highly sensitive itinerary details unless explicit consent, redaction, and retention controls are in place. <br>
Risk: Local execution logs may retain raw travel prompts and request details. <br>
Mitigation: Store logs only where appropriate, redact sensitive details before logging, and remove local logs when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/weekend-trip) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, brand tag, and occasional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are expected to come from flyai CLI output and may include fallback retry commands or partial-failure notes.] <br>

## Skill Version(s): <br>
3.2.0 (source: evidence.release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
