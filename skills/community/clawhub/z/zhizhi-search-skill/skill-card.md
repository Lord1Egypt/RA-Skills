## Description:

Use when the user needs a specific answer from the web and that answer can be judged right or wrong — fact-checking, source hunting, and looking up details all count.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuworks](https://clawhub.ai/user/wuworks)

### License/Terms of Use:

MIT-0

## Use Case:

People using an AI agent for factual web research use this skill to search for the user's exact subject, check each round for drift, and report whether the results matched, drifted, or were not found.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A clean scanner verdict does not guarantee zero risk.

Mitigation: Review the skill and decide whether it suits the intended use before installing.

Risk: Search results may relate to a nearby subject rather than the user's exact question, which could lead to a misleading answer if the drift is not reported.

Mitigation: Check every round against the captured subject; on Drifted or Not found, stop, state what was found, and ask whether to change direction.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wuworks/skills/zhizhi-search)
- [Server-resolved source repository and skill path](https://github.com/WuWorks/zhizhi-search-skill/tree/main/zhizhi-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise natural-language report with a verdict, reason, and source summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports Matched, Drifted, or Not found; on Drifted or Not found, stops searching and asks whether to change direction.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
