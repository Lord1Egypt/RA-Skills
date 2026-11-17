## Description:

Social intelligence for agents that maintains a per-person network graph with trust levels, topic boundaries, sharing rules, and a sharing log to help avoid repeated or poorly timed disclosures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mculp](https://clawhub.ai/user/mculp)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to organize social context about people, topic boundaries, and prior sharing so conversations can be more considerate and less repetitive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent per-person records can accumulate private or sensitive details about real people.

Mitigation: Keep entries minimal, avoid secrets and sensitive traits, get consent where appropriate, and review and delete records regularly.

Risk: The sharing log can preserve details from past conversations longer than users or contacts expect.

Mitigation: Record only what is needed to avoid repetition and remove stale or unnecessary conversation history.

Risk: Broad activation could influence unrelated conversations with stored social assumptions.

Mitigation: Narrow activation to explicit social-graph tasks and review notes before relying on them.

## Reference(s):

- [Social Network Graph Template](artifact/references/network-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces non-executable social reasoning guidance and suggested Markdown records for network and sharing history.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
