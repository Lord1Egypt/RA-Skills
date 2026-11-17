## Description:

Smart Search Fallback routes an agent's web search request across configured search, crawling, browser, and direct-fetch tools, then falls back to the next available option when a preferred tool fails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate web search and content retrieval workflows when search requests require fallback across multiple tools or providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that crafted query text can execute as Python code in one fallback path.

Mitigation: Fix the fallback script to pass query text as data rather than interpolating it into Python source, and avoid untrusted or sensitive queries until that change is made.

Risk: Search queries may be sent to several third-party search, crawling, browser, or fetch tools.

Mitigation: Avoid sensitive query text unless each configured provider and local credential path is approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tuobadaidai/skills/smart-search-fallback)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with bash, Python, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke third-party search and crawling tools; some paths depend on optional API keys and local tool availability.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
