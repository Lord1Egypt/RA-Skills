## Description:

Analyzes a given URL and automatically generates comprehensive functional, UI, and boundary test cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kushanlk](https://clawhub.ai/user/kushanlk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quality engineers use this skill to generate Markdown test plans for a target URL, including functional, UI, and boundary coverage based on interactive DOM elements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analyzer script is empty, so the skill may fail or produce no useful DOM evidence for test generation.

Mitigation: Implement and review analyze-dom.js before relying on generated test plans, then verify outputs against the target application.

Risk: Future Playwright-based browsing could access sensitive internal or authenticated pages if used without boundaries.

Mitigation: Pin Playwright, review future analyzer changes, and limit execution to approved non-sensitive test environments or URLs.

## Reference(s):


## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown test plan with steps to reproduce, expected results, and edge cases.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Takes a target URL and depends on DOM analysis from analyze-dom.js; the current artifact includes an empty analyzer script.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
