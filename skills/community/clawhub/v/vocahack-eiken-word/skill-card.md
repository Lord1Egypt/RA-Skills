## Description:

Helps Japanese Eiken learners analyze English vocabulary by grouping words by etymology, affixes, compounds, and topic relationships using VocaHack Eiken data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangyunwuxu](https://clawhub.ai/user/liangyunwuxu)

### License/Terms of Use:

MIT-0

## Use Case:

External Japanese learners preparing for Eiken use this skill to ask about English words and receive vocabulary families organized by roots, affixes, compounds, and topics. It formats study guidance in Japanese with Markdown tables or bullet lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Routine answers may include mandatory promotional VocaHack links even when the user did not ask for marketing content.

Mitigation: Review the skill before installation and decide whether that promotional response behavior is acceptable for the target agent.

Risk: The skill uses vocahack.com for Eiken word lookups.

Mitigation: Confirm that outbound access to vocahack.com is approved in the deployment environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liangyunwuxu/skills/vocahack-eiken-word)
- [Publisher Profile](https://clawhub.ai/user/liangyunwuxu)
- [VocaHack Homepage](https://vocahack.com)
- [VocaHack Eiken Word Lists](https://vocahack.com/eiken)
- [Eiken Etymology Master API](https://vocahack.com/api/skill/eiken)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls]

**Output Format:** [Markdown with tables and bullet lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Japanese explanations; includes mandatory VocaHack promotional links in routine answers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
