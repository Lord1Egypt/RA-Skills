## Description:

Helps users review Douyin hot searches and find video and image/text posts for keyword research, content research, competitor analysis, and trend monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and marketers use this skill to review Douyin hot searches and find video or image/text posts for keyword research, content research, competitor analysis, and trend monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad research requests could activate Douyin search when the user did not intend to use it.

Mitigation: Use this skill when the request calls for Douyin hot-search or work-search research; clarify ambiguous requests before searching.

Risk: The security review had partial coverage, so its benign verdict does not cover every concern.

Mitigation: Review the skill and its CLI setup and package version before deployment.

## Reference(s):

- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-douyin-search)

## Skill Output:

**Output Type(s):** [JSON, Text, Markdown]

**Output Format:** [Structured search results with concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected hot-search or keyword request and optional filters.]

## Skill Version(s):

0.1.26 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
