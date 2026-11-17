## Description:

Audits SwiftUI runtime performance through code review, architecture analysis, and user-guided Instruments profiling for slow rendering, janky scrolling, high CPU or memory use, excessive view updates, and layout thrash.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soponcd](https://clawhub.ai/user/soponcd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit SwiftUI views and data flow, identify likely causes of runtime slowdowns, and produce prioritized fixes or profiling guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill can involve sharing app source code, profiler traces, or screenshots with an agent.

Mitigation: Share only project details you are comfortable having analyzed, and redact secrets, customer data, and proprietary material that is not needed for the audit.

Risk: Performance conclusions may be incomplete when based only on code review, symptoms, or screenshots.

Mitigation: Use the skill's profiling workflow to collect comparable Instruments data and verify changes against baseline metrics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soponcd/skills/timeflow-swiftui-performance-audit)
- [Skill homepage](https://github.com/soponcd/timeflow-skills/tree/main/teams/skills/swiftui-performance-audit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with issue lists, metrics tables when available, Swift code snippets, and profiling instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include before/after metrics when traces or measurements are provided.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
