## Description:

择日学技能 supports Chinese almanac-style date selection, including auspicious and inauspicious days, Jianchu twelve deities, Huangdao/Heidao indicators, Shen Sha influences, and suggestions for events such as weddings, openings, ground-breaking, and travel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dglijin-oss](https://clawhub.ai/user/dglijin-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to provide Chinese-language date-selection guidance for culturally specific planning tasks such as weddings, business openings, construction starts, travel, and general auspicious-day checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill appears to produce Chinese-only guidance.

Mitigation: Deploy it only where Chinese-language output is acceptable, or require translation and localization review before user-facing release.

Risk: The documented Python entrypoint is absent and the bundled JavaScript does not pass a syntax check, so the skill may not run as documented.

Mitigation: Validate the runtime path in a staging agent before enabling it, and require a corrected artifact if executable behavior is needed.

Risk: Date-selection recommendations may be culturally specific and should not be treated as factual, legal, medical, financial, or safety-critical advice.

Mitigation: Present outputs as traditional almanac-style guidance and require human judgment for consequential decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dglijin-oss/skills/ze-ri-skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese-language text or Markdown date-selection guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include auspiciousness labels, Yi/Ji recommendations, conflict indicators, event-specific recommendations, and scoring.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
