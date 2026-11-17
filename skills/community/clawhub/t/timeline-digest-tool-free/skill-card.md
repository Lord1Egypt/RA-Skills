## Description: <br>
时间线摘要工具-免费版 uses an authenticated bird/X session to read For You and Following timelines, deduplicate and filter posts, and produce a structured JSON digest for personal information aggregation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and individual operators use this skill to run local X/Twitter timeline digest workflows over their authenticated session. It is intended for daily information aggregation, topic tracking, and reducing duplicate or low-value timeline noise. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an authenticated bird/X session to read timeline data. <br>
Mitigation: Enable it only for intended X/Twitter digest workflows and avoid using it for unrelated analytics tasks. <br>
Risk: The workflow writes local digest and state files that may retain timeline-derived identifiers or metadata. <br>
Mitigation: Review the configured statePath and delete retained state when it is no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with shell command examples and structured JSON digest output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local state files for incremental filtering and expects bird CLI authentication for X/Twitter timeline access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
