## Description:

Launches background Clawdbot sessions to research business ideas and return a comprehensive Markdown report with market, technical, go-to-market, risk, validation, and recommendation analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rqrqrqrq](https://clawhub.ai/user/rqrqrqrq)

### License/Terms of Use:


## Use Case:

Developers and Clawdbot users use this skill to start autonomous business-idea research from chat and receive actionable market, technical, business-model, go-to-market, risk, validation, and verdict guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted ideas and generated reports may be stored locally under ~/clawd/ideas/ and sent back through the chat.

Mitigation: Avoid highly confidential business ideas unless local storage and chat delivery are acceptable for the workspace.

Risk: Spawned research sessions may be kept for later review and retain context about the submitted idea.

Mitigation: Review retained sessions and reports according to workspace data-handling expectations.

Risk: Market research, pricing benchmarks, and competitor analysis can be stale or incomplete.

Mitigation: Verify cited sources and key assumptions before using the report for business decisions.

## Reference(s):

- [Research Idea ClawHub skill page](https://clawhub.ai/rqrqrqrq/skills/research-idea)
- [Publisher profile](https://clawhub.ai/user/rqrqrqrq)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown research report plus a short chat summary and verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save reports under ~/clawd/ideas/<slug>/research.md and keep spawned sessions for later review.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
