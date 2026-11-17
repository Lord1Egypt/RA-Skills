## Description:

Finds TikTok Shop creators associated with a specified store ID using Qinghu data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shop operators and market researchers use this skill to identify creators promoting a TikTok Shop store and assess competitor creator partnerships.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or upgrade Node and qhkit and modify the local PATH.

Mitigation: Require explicit approval for setup or upgrades; prefer a pinned qhkit version in an isolated environment.

Risk: Configuring qhkit can store an API token locally.

Mitigation: Get explicit approval before configuring credentials and keep the token out of chat and logs.

Risk: Creator lookups incur variable credit charges, including potentially larger charges for bulk results.

Mitigation: Estimate costs first, explain potential charges, and obtain approval before paid or bulk calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-tiktok-shop-creators)
- [Qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise answer with a brief preview; table file for 10 or more records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports credits spent on paid calls; creator details require a separate lookup.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
