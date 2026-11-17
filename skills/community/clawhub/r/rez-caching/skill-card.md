## Description:

Guides developers through diagnosing Rez 3.4.0 resolve and package caching, inspecting cache settings, and addressing stale entries or slow resolves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to identify which Rez cache is active, troubleshoot package changes that seem to be ignored, and measure the effect of caching on resolves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flushing a shared resolve cache can temporarily slow subsequent solves.

Mitigation: Check cache settings and bypass the resolve cache for one run before reviewing rez-memcache --flush on shared infrastructure.

Risk: Cleaning the package cache removes local cached files and may increase subsequent load times.

Mitigation: Identify the affected variant first, then review rez-pkg-cache -r and --clean before running them.

## Reference(s):

- [rez-caching on ClawHub](https://clawhub.ai/loonghao/skills/rez-caching)
- [memcached](https://memcached.org/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers Rez 3.4.0.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
