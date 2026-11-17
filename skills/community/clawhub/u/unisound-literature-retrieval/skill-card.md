## Description:

Supports clinical literature question answering and retrieval planning by aligning user-provided citation or abstract excerpts to PICO and summarizing evidence narratives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians and clinical researchers use this skill to turn clinical questions and optional literature excerpts into PICO framing, evidence narrative, and next-step search suggestions for study planning, review outlines, or briefing drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical questions, constraints, and provided literature excerpts are sent to the documented Hivoice API.

Mitigation: Avoid patient identifiers and confidential clinical details in inputs unless the deployment has approved that data flow.

Risk: The app key is accepted as a command-line argument, which may expose credentials through shell or process history.

Mitigation: Use a safer secret-injection path when deploying, such as an approved secret manager or environment-controlled wrapper.

Risk: The skill is not a real-time literature index and may produce strategy-level guidance when no passages are provided.

Mitigation: Distinguish unanchored retrieval suggestions from evidence grounded in supplied excerpts, and require human review before clinical or research decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-literature-retrieval)
- [Hivoice chat completions API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [JSON object with Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes PICO framing, evidence notes, retrieval-extension suggestions, and limitation notes based on the provided question and optional passages.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
