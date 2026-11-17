## Description:

Extracts structured Q&A pairs and selection preferences from chat sessions, documents, articles, transcripts, or other freeform text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a conversation or supplied text into reusable Q&A records and stated or inferred selection preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation or document content may include sensitive personal, business, legal, medical, or credential information that the skill summarizes into reusable Q&A and preference records.

Mitigation: Invoke it only on content the user explicitly wants summarized, and avoid sensitive material unless that reuse is intended.

Risk: Inferred preferences or synthesized answers may misstate the source material if used without review.

Mitigation: Review generated Q&A pairs and preference labels before using them as a knowledge base, quiz source, or decision record.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with Q&A and preference table sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes total counts and labels preferences as direct or inferred.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
