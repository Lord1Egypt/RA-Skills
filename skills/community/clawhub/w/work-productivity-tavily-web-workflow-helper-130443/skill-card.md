## Description:

Helps agent users and skill authors plan, implement, and validate Tavily-style web-search productivity workflows, including bug fixes, setup hardening, reliability improvements, and adjacent workflow artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, developers, and skill authors use this skill to turn Tavily-style web-search productivity needs into practical plans, checklists, code changes, configuration guidance, and validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad invocation terms may cause the skill to activate for ordinary web, search, API, or workflow requests where a narrower helper would be more appropriate.

Mitigation: Review invocation keywords and prompts before deployment, and narrow activation terms to Tavily-style work-productivity and web-workflow support.

Risk: The skill provides guidance and generated artifacts, so incorrect assumptions could lead to unsuitable plans, code, shell commands, or configuration advice.

Mitigation: Ask for materially missing context, state assumptions, and validate the final output against the user's success criteria before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-tavily-web-workflow-helper-130443)
- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub Skill Demand: Tavily Search](https://clawhub.ai/skills/openclaw-tavily-search)
- [Popular ClawHub Skill Demand: Multi Search Engine](https://clawhub.ai/skills/multi-search-engine)
- [How Google decided to Destroy its Search Monopoly](https://news.ycombinator.com/item?id=48945074)
- [Why I Built Another Open Source Agent](https://www.v2ex.com/t/1228101)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text, with code blocks and checklists when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, and follow-up risks for the user's workflow.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
