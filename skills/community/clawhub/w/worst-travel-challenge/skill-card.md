## Description:

Plans intentionally poor travel challenge itineraries using FlyAI travel search, with snarky commentary, booking links, photo explanations, a trip diary, and short-video scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catshcrozhang](https://clawhub.ai/user/catshcrozhang)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to create deliberately uncomfortable, parody-style travel plans from FlyAI travel data, then turn the trip into shareable commentary, diary, report, and short-video script content. The skill asks for travel basics, proposes transport, lodging, and activity options, and includes a rescue mode when the user wants to switch to higher-quality choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on installing the FlyAI CLI globally, and the dependency is not pinned in the artifact instructions.

Mitigation: Install the CLI only from a trusted source, review the installed package and version, and manage updates through a controlled environment.

Risk: Travel searches can send destination, date, budget, and preference details to FlyAI.

Mitigation: Avoid entering sensitive personal details unless necessary, and review the FlyAI service terms and data handling before use.

Risk: Generated booking links can lead to real commercial purchases for intentionally poor or randomized travel choices.

Mitigation: Manually verify destination, dates, traveler details, total cost, cancellation terms, safety, health constraints, and budget before clicking or purchasing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/catshcrozhang/skills/worst-travel-challenge)
- [FlyAI Open Platform](https://flyai.open.fliggy.com)
- [Detailed Reference](artifact/references/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style itinerary sections, booking-link summaries, trip diary/report content, and short-video script templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include real travel booking links that require user review before purchase.]

## Skill Version(s):

1.1.5 (source: ClawHub release evidence; artifact frontmatter reports 1.1.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
