## Description:

Generates 60 high-impact tweet ideas from reference content across 5 categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentchan](https://clawhub.ai/user/vincentchan)

### License/Terms of Use:


## Use Case:

Content creators, marketers, and social media teams use this skill to turn supplied drafts, notes, files, pasted text, or URLs into categorized Twitter/X post ideas with short explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided URLs may be fetched over the network.

Mitigation: Review URLs before use and avoid private or internal URLs unless you intend the agent to process them.

Risk: Private drafts, unpublished notes, or sensitive material may be processed and saved into a local markdown output file.

Mitigation: Provide only material approved for agent processing and review the generated file before sharing it.

Risk: The output may contain fewer than 60 ideas if the source material does not support every requested category.

Mitigation: Supply richer reference material or accept category skipping when the content does not fit a category.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vincentchan/skills/tweet-ideas-generator)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown file with categorized tweet ideas, explanations, analysis notes, and a source-material summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves output to tweet-ideas/tweets-{timestamp}.md; statements are intended to stay under 280 characters when possible.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
