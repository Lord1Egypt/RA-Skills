## Description:

Generates and pre-scores email subject-line and preheader variants using heuristic spam-trigger, truncation, emoji, and inbox-preview checks before A/B testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators and email teams use this skill to draft or screen subject-line and preheader variants for promo, lifecycle, cold-outbound, and newsletter campaigns before selecting candidates for testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted campaign exports or subject candidates may include sensitive marketing context, and the skill may propose saving useful results to memory.

Mitigation: Provide only approved campaign data and allow memory writes only after confirming that retaining the marketing context is acceptable.

Risk: Heuristic spam-trigger and truncation checks may be mistaken for a deliverability guarantee.

Mitigation: Treat the pre-score as triage only, and use a full deliverability or quality audit before relying on inbox-placement, authentication, or veto conclusions.

Risk: Generated subject lines can introduce unsupported statistics, discounts, scarcity, or personalization claims.

Mitigation: Require source evidence for factual or scarcity claims and keep unsupported hooks marked as needing a source.

## Reference(s):

- [Subject Line Lab on ClawHub](https://clawhub.ai/aaron-he-zhu/skills/subject-line-lab)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Spam-Trigger Checklist](references/spam-trigger-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown tables and handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes variant ids, angle labels, heuristic flags, inbox preview renders, a ranked shortlist, and an optional memory handoff summary.]

## Skill Version(s):

19.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
