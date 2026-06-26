## Description: <br>
Push real-time progress and key metrics to a live statb.io dashboard during long-running, multi-step, or iterative agent tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qianlong2005](https://clawhub.ai/user/qianlong2005) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to expose numeric progress counters, rates, errors, timings, and other task metrics on a live browser dashboard while work is running. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Progress counters and task metrics are sent to statb.io and may be visible to anyone with the board URL. <br>
Mitigation: Use explicit consent before enabling it on private work, keep board IDs and metric keys generic, and never push secrets, tokens, PII, or sensitive task details. <br>
Risk: A board can become misleading if the agent pushes only an initial update or stops updating during the work. <br>
Mitigation: Push updates at meaningful intervals or inside loops, and send a final status update when the task completes. <br>


## Reference(s): <br>
- [statb.io homepage](https://statb.io) <br>
- [ClawHub skill page](https://clawhub.ai/qianlong2005/statb) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and URL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates curl-based progress updates using numeric key-value metrics; statb.io free tier supports up to 16 metrics per board.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
