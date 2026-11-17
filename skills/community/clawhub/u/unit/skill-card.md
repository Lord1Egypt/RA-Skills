## Description:

Unit converts common measurement units, temperatures, data storage values, and live currency exchange rates for agent responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlang-cn](https://clawhub.ai/user/openlang-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to answer unit conversion requests across everyday measurement categories, temperature formulas, and live currency rates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Currency conversions contact exchangerate.host and exchange rates can change.

Mitigation: Expect network access for currency requests and verify rates before using results for transactions.

Risk: The converter writes a small cache file under the user's home directory.

Mitigation: Run the skill in an isolated environment when local file writes need to be constrained.

Risk: The requests dependency is declared with a minimum version rather than a pinned exact version.

Mitigation: Use a virtual environment and pin dependencies during deployment.

## Reference(s):

- [Unit ClawHub release](https://clawhub.ai/openlang-cn/skills/unit)
- [exchangerate.host](https://exchangerate.host)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text conversion results and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Currency conversion may perform a live HTTP lookup and cache rates for one hour.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
