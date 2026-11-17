## Description:

Analyzes multi-pet images or videos to classify social behaviors such as sniffing, chasing, biting, fleeing, hiding, and playing, then returns a structured interaction report with durations, frequencies, participants, and potential conflict indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External pet owners, pet boarding centers, pet daycare teams, and animal behavior clinics use this skill to review multi-pet media, quantify interaction patterns, and identify possible aggression or stress signals for observation-oriented reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends pet media and report requests to the publisher's cloud service.

Mitigation: Use only media appropriate for third-party processing, obtain consent for shared household, clinic, daycare, or boarding-center footage, and confirm retention and deletion practices before deployment.

Risk: The skill silently creates or reuses an account identity and stores service tokens or user records in the workspace data directory.

Mitigation: Run it in an isolated workspace or account, restrict access to workspace data, and clear stored credentials and user records after use when operationally appropriate.

Risk: The skill can retrieve cloud-hosted history for the resolved account identity.

Mitigation: Gate history-list workflows behind explicit user intent and verify account and tenant isolation before enabling use with sensitive footage.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-social-interaction-analysis-analysis)
- [API 接口文档](references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Markdown text containing structured JSON-like analysis content and report links; optional file output when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return a structured analysis report or a history list for the resolved account identity.]

## Skill Version(s):

1.0.8 (source: server release metadata; artifact frontmatter says 1.0.12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
