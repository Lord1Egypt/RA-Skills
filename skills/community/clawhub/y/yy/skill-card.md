## Description: <br>
Organizes and summarizes public YY Live pages, including live categories, activity pages, streamer rules, and help documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codenova58](https://clawhub.ai/user/codenova58) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect and summarize public YY Live activity, category, streamer-rule, safety, and help information without accessing private account or backend data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A bundled review helper was reported as broader than needed because it can launch nested Codex with full filesystem access and approval bypass. <br>
Mitigation: Review before installing; if used, run the helper with sandbox-preserving settings such as --no-yolo unless elevated local access is intentional. <br>
Risk: YY Live activities, rules, and help pages may change frequently. <br>
Mitigation: Include retrieval dates and source links in summaries, and avoid treating prior summaries as current policy. <br>
Risk: The skill could be misused to request view boosting, gift manipulation, account control, or risk-avoidance guidance. <br>
Mitigation: Keep responses limited to public information organization and refuse requests for manipulation, account takeover, private data, or platform rule evasion. <br>


## Reference(s): <br>
- [YY Live homepage](https://www.yy.com/) <br>
- [ClawHub skill page](https://clawhub.ai/codenova58/yy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summaries, tables, and checklists with source links when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should timestamp public YY Live information because platform activities and rules can change frequently.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
