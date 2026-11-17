## Description:

Real-time football transfer intelligence — rumours, credibility scores, and multi-source verification

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeleon](https://clawhub.ai/user/leeleon)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to retrieve trending football transfer rumours, detailed player transfer intelligence, and Truth Meter credibility scores from Rising Transfers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Player and club search terms are sent to Rising Transfers for transfer lookup and credibility queries.

Mitigation: Install only if you trust Rising Transfers with those search terms and avoid submitting sensitive or unrelated information.

Risk: Authenticated detailed intelligence and Truth Meter queries can consume plan credits.

Mitigation: Use hot topics for no-credit checks when sufficient, and confirm RT_API_KEY usage before detailed or credibility queries.

Risk: The skill may be invoked automatically for transfer news, rumour, or credibility prompts.

Mitigation: Disable skill auto-discovery when you want the integration used only by explicit request.

Risk: Football transfer rumours can be incomplete or unavailable for a requested player or club.

Mitigation: Report unavailable results clearly and do not fabricate transfer details, probability scores, or source evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leeleon/skills/rising-transfers-transfer-intel)
- [Rising Transfers API](https://api.risingtransfers.com)
- [Rising Transfers API docs](https://api.risingtransfers.com/docs)
- [Rising Transfers pricing](https://api.risingtransfers.com/pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries with transfer lists, credibility scores, source summaries, and error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require RT_API_KEY for detailed and credibility queries; hot topics can run without a key.]

## Skill Version(s):

1.0.0 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
