## Description:

What worked here, and how do I do it again? Which tool and route succeeded on this host, and is it repeatable? Use this after finally succeeding on a difficult host, when asked to make a result repeatable, or before writing a workspace skill for a recurring task. Ranks the tool, method and route combinations that succeeded on a host with lower confidence bounds and latency and returns a recipe. Returns exactly WRITE_SKILL, POST_WITNESS_CARD or NOTHING_PROVEN_YET. Do not use on hosts with fewer than three observed requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill after a difficult success to identify the repeatable tool, method, and route combination recorded for a host, then decide whether to write a reusable workspace skill or post a witness card.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the ClawPhylax plugin as a local ledger of request outcomes.

Mitigation: Install it only when comfortable with that local ledger model, check plugin status before use, and proceed without verification if the plugin is unavailable.

Risk: A suggested recipe can overstate repeatability when too few observations exist or routes differ below the grouping depth.

Mitigation: Ignore hosts or combinations with fewer than three observations and review the selected tool, method, route, lower bound, and latency before reusing the recipe.

Risk: The skill may lead an agent to write a workspace skill or offer a witness card based on prior outcomes.

Mitigation: Require user approval before writing a skill or posting a witness card, and scan or review generated skill content before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aeneassoft/skills/what-worked-here)
- [ClawPhylax project homepage](https://github.com/aeneassoft/clawphylax)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with an action line, recipe details, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The first line is ACTION: WRITE_SKILL, ACTION: POST_WITNESS_CARD, or ACTION: NOTHING_PROVEN_YET.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
