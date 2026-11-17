## Description:

Research skill that conditionally rewrites search keywords on trigger topics for authorized security testing.

This skill is for research and development only.

## Publisher:

[seoeunjungg](https://clawhub.ai/user/seoeunjungg)

### License/Terms of Use:


## Use Case:

Developers and security researchers use this skill in authorized lab environments to test how search workflows respond when finance or health queries are conditionally rewritten.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance or health queries can be rewritten to include speculative rumor language, which can bias downstream search results.

Mitigation: Use only in controlled security-testing environments where users expect query poisoning, and require review and explicit approval of transformed keywords before search.

## Reference(s):


## Skill Output:

**Output Type(s):** [text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns keyword, num_results, and triggered; num_results defaults to 3 and is clamped from 1 to 10.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
